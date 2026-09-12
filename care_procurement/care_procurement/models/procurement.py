import uuid

from django.core.exceptions import ValidationError
from django.db import models


class ProcurementModel(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    facility_id = models.UUIDField()
    deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vendor(ProcurementModel):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return self.name


class Tender(ProcurementModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        AWARDED = "awarded", "Awarded"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    awarded_vendor = models.ForeignKey(
        Vendor, null=True, blank=True, on_delete=models.PROTECT, related_name="awarded_tenders"
    )

    def transition_to(self, status):
        allowed = {
            self.Status.DRAFT: {self.Status.PUBLISHED},
            self.Status.PUBLISHED: {self.Status.AWARDED},
            self.Status.AWARDED: {self.Status.CLOSED},
            self.Status.CLOSED: set(),
        }
        if status not in allowed[self.status]:
            raise ValidationError(f"Cannot move tender from {self.status} to {status}.")
        self.status = status


class PurchaseOrder(ProcurementModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        APPROVED = "approved", "Approved"
        RECEIVED = "received", "Received"
        CANCELLED = "cancelled", "Cancelled"

    number = models.CharField(max_length=40)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="purchase_orders")
    tender = models.ForeignKey(
        Tender, null=True, blank=True, on_delete=models.PROTECT, related_name="purchase_orders"
    )
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def transition_to(self, status):
        allowed = {
            self.Status.DRAFT: {self.Status.APPROVED, self.Status.CANCELLED},
            self.Status.APPROVED: {self.Status.RECEIVED, self.Status.CANCELLED},
            self.Status.RECEIVED: set(),
            self.Status.CANCELLED: set(),
        }
        if status not in allowed[self.status]:
            raise ValidationError(f"Cannot move purchase order from {self.status} to {status}.")
        self.status = status


class Receipt(ProcurementModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, related_name="receipts"
    )
    received_date = models.DateField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def transition_to(self, status):
        if self.status != self.Status.PENDING or status not in {
            self.Status.ACCEPTED,
            self.Status.REJECTED,
        }:
            raise ValidationError(f"Cannot move receipt from {self.status} to {status}.")
        self.status = status
