from rest_framework import serializers

from care_procurement.models import PurchaseOrder, Receipt, Tender, Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["external_id", "facility_id", "name", "contact_email", "contact_phone"]
        read_only_fields = ["external_id"]


class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = [
            "external_id", "facility_id", "title", "description", "status", "awarded_vendor",
        ]
        read_only_fields = ["external_id"]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = [
            "external_id", "facility_id", "number", "vendor", "tender", "description",
            "status", "total_amount",
        ]
        read_only_fields = ["external_id"]


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = [
            "external_id", "facility_id", "purchase_order", "received_date", "notes", "status",
        ]
        read_only_fields = ["external_id"]
