from django.db import models
from django.conf import settings

from assets.models import Asset
from django.core.exceptions import ValidationError

class Booking(models.Model):

    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Ongoing", "Ongoing"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    resource = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE
    )

    booked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    purpose = models.TextField()

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Upcoming"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):

        overlapping_booking = Booking.objects.filter(
            resource=self.resource,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)

        if overlapping_booking.exists():
            raise ValidationError(
                "This resource is already booked for the selected time slot."
            )
    
    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.resource.asset_tag} - {self.booked_by.username}"