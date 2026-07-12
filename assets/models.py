from django.db import models
from django.conf import settings

from core.models import Department, AssetCategory
from notifications.models import Notification
from django.core.exceptions import ValidationError


class Asset(models.Model):

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Allocated", "Allocated"),
        ("Maintenance", "Maintenance"),
        ("Lost", "Lost"),
        ("Disposed", "Disposed"),
    ]

    CONDITION_CHOICES = [
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Damaged", "Damaged"),
    ]

    asset_tag = models.CharField(max_length=20, unique=True, blank=True)

    asset_name = models.CharField(max_length=150)

    category = models.ForeignKey(
        AssetCategory,
        on_delete=models.CASCADE
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    manufacturer = models.CharField(
        max_length=100,
        blank=True
    )

    model_number = models.CharField(
        max_length=100,
        blank=True
    )

    serial_number = models.CharField(
        max_length=100,
        unique=True
    )

    purchase_date = models.DateField()

    warranty_expiry = models.DateField(
        null=True,
        blank=True
    )

    purchase_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    current_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=150
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Available"
    )

    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default="Excellent"
    )

    image = models.ImageField(
        upload_to="assets/",
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.asset_tag:

            last_asset = Asset.objects.order_by("id").last()

            if last_asset:
                asset_id = last_asset.id + 1
            else:
                asset_id = 1

            self.asset_tag = f"AF-{asset_id:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.asset_tag} - {self.asset_name}"
    
class AssetAllocation(models.Model):

    STATUS_CHOICES = [
        ("Allocated", "Allocated"),
        ("Returned", "Returned"),
    ]

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE
    )

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="allocated_assets"
    )

    allocated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="allocated_by"
    )

    allocated_date = models.DateField(auto_now_add=True)

    expected_return_date = models.DateField(
        null=True,
        blank=True
    )

    actual_return_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Allocated"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )



    return_requested = models.BooleanField(
        default=False
    )

    return_approved = models.BooleanField(
        default=False
    )

    condition_check = models.CharField(
        max_length=100,
        blank=True
    )

    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="received_assets"
    )

    def clean(self):

        if self.status == "Allocated":

            already_allocated = AssetAllocation.objects.filter(
                asset=self.asset,
                status="Allocated"
            ).exclude(pk=self.pk)

            if already_allocated.exists():
                raise ValidationError({
                    "asset": "This asset is already allocated."
                })

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

        Notification.objects.create(
            user=self.employee,
            title="Asset Allocated",
            message=f"You have been assigned {self.asset.asset_name} ({self.asset.asset_tag})."
        )

        if self.status == "Allocated":
            self.asset.status = "Allocated"

        elif self.status == "Returned":

            if self.return_approved:

                self.asset.status = "Available"

                self.asset.assigned_to = None

            else:

                self.asset.status = "Allocated"

        self.asset.save()

    def __str__(self):
        return f"{self.asset.asset_tag} → {self.employee.username}"