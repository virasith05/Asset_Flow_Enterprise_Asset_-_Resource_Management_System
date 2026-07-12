from django.db import models
from django.conf import settings

from assets.models import Asset


class MaintenanceRecord(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Assigned", "Assigned"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
        ("Rejected", "Rejected"),
    ]

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE
    )

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    issue = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )

    maintenance_date = models.DateField(auto_now_add=True)

    expected_completion = models.DateField(
        null=True,
        blank=True
    )

    completion_date = models.DateField(
        null=True,
        blank=True
    )

    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_jobs"
    )

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
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

        super().save(*args, **kwargs)

        if self.status in [
            "Pending",
            "Approved",
            "Assigned",
            "In Progress"
        ]:
            self.asset.status = "Maintenance"

        elif self.status == "Resolved":
            self.asset.status = "Available"

        elif self.status == "Rejected":
            self.asset.status = "Available"
        self.asset.save()

    def __str__(self):
        return f"{self.asset.asset_tag} - {self.status}"