from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from care_procurement.models import PurchaseOrder, Receipt, Tender


class ProcurementTransitionTests(SimpleTestCase):
    def test_tender_follows_ordered_lifecycle(self):
        tender = Tender(status=Tender.Status.DRAFT)
        tender.transition_to(Tender.Status.PUBLISHED)
        tender.transition_to(Tender.Status.AWARDED)
        tender.transition_to(Tender.Status.CLOSED)
        self.assertEqual(tender.status, Tender.Status.CLOSED)

    def test_purchase_order_cannot_skip_approval(self):
        order = PurchaseOrder(status=PurchaseOrder.Status.DRAFT)
        with self.assertRaises(ValidationError):
            order.transition_to(PurchaseOrder.Status.RECEIVED)

    def test_receipt_has_one_terminal_decision(self):
        receipt = Receipt(status=Receipt.Status.PENDING)
        receipt.transition_to(Receipt.Status.ACCEPTED)
        with self.assertRaises(ValidationError):
            receipt.transition_to(Receipt.Status.REJECTED)
