"""URL routes.

Core mounts this module at /api/care_procurement/ via the PLUGIN_APPS loop in
config/urls.py. Do not repeat that prefix here.

Routes under `otp/` are for the patient portal (OTP-authenticated, phone-number scoped).
Keep them read-mostly. See the care-auth-contexts skill.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from care_procurement.viewsets.config import ConfigView
from care_procurement.viewsets.procurement import (
    PurchaseOrderViewSet,
    ReceiptViewSet,
    TenderViewSet,
    VendorViewSet,
)

router = DefaultRouter()
router.register("vendors", VendorViewSet, basename="procurement-vendor")
router.register("tenders", TenderViewSet, basename="procurement-tender")
router.register("purchase-orders", PurchaseOrderViewSet, basename="procurement-purchase-order")
router.register("receipts", ReceiptViewSet, basename="procurement-receipt")

urlpatterns = [
    *router.urls,
    path("config/", ConfigView.as_view(), name="care_procurement-config"),
]
