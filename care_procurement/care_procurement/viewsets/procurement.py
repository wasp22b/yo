from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from care_procurement.models import PurchaseOrder, Receipt, Tender, Vendor
from care_procurement.serializers.procurement import (
    PurchaseOrderSerializer,
    ReceiptSerializer,
    TenderSerializer,
    VendorSerializer,
)


class FacilityScopedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = "external_id"

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        facility_id = self.request.query_params.get("facility")
        return queryset.filter(facility_id=facility_id) if facility_id else queryset.none()

    @action(detail=True, methods=["post"])
    def transition(self, request, external_id=None):
        instance = self.get_object()
        try:
            instance.transition_to(request.data.get("status"))
        except DjangoValidationError as exc:
            raise ValidationError({"status": exc.messages}) from exc
        instance.save(update_fields=["status", "modified_date"])
        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)


class VendorViewSet(FacilityScopedViewSet):
    model = Vendor
    serializer_class = VendorSerializer


class TenderViewSet(FacilityScopedViewSet):
    model = Tender
    serializer_class = TenderSerializer


class PurchaseOrderViewSet(FacilityScopedViewSet):
    model = PurchaseOrder
    serializer_class = PurchaseOrderSerializer


class ReceiptViewSet(FacilityScopedViewSet):
    model = Receipt
    serializer_class = ReceiptSerializer
