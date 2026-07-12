from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    phone = models.CharField(max_length=15, blank=True)

    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Asset Manager", "Asset Manager"),
        ("Department Head", "Department Head"),
        ("Employee", "Employee"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="Employee",
    )

    is_active_employee = models.BooleanField(default=True)

    def __str__(self):
        return self.username