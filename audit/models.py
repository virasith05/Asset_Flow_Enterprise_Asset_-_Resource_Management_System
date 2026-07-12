from django.db import models
from django.conf import settings


class AuditLog(models.Model):

    ACTION_CHOICES = [
        ("Create", "Create"),
        ("Update", "Update"),
        ("Delete", "Delete"),
        ("Allocate", "Allocate"),
        ("Return", "Return"),
        ("Maintenance", "Maintenance"),
        ("Login", "Login"),
        ("Logout", "Logout"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES
    )

    module = models.CharField(
        max_length=50
    )

    description = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user} - {self.action}"