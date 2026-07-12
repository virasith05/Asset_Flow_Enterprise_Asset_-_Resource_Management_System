from django.db import models
from django.conf import settings

from assets.models import Asset
from datetime import date
from assets.models import AssetAllocation

class TransferRequest(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE
    )

    from_employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transfer_from"
    )

    to_employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transfer_to"
    )

    reason = models.TextField()

    requested_date = models.DateField(
        auto_now_add=True
    )

    approved_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        # Check previous status before saving
        old_status = None

        if self.pk:
            old_status = TransferRequest.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        # Execute transfer only once
        if self.status == "Approved" and old_status != "Approved":

            # Close current allocation
            current = AssetAllocation.objects.filter(
                asset=self.asset,
                status="Allocated"
            ).first()

            if current:
                current.status = "Returned"
                current.actual_return_date = date.today()
                current.save()

            # Create new allocation
            AssetAllocation.objects.create(
                asset=self.asset,
                employee=self.to_employee,
                allocated_by=self.from_employee,
                status="Allocated"
            )

            # Update asset
            self.asset.assigned_to = self.to_employee
            self.asset.status = "Allocated"
            self.asset.save()

            # Save approval date
            self.approved_date = date.today()
            super().save(update_fields=["approved_date"])
    def __str__(self):
        return f"{self.asset.asset_tag} → {self.to_employee.username}"