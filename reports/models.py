from django.db import models


class Report(models.Model):

    REPORT_TYPES = [
        ("Asset Summary", "Asset Summary"),
        ("Department Summary", "Department Summary"),
        ("Maintenance Summary", "Maintenance Summary"),
        ("Allocation Summary", "Allocation Summary"),
    ]

    report_type = models.CharField(
        max_length=50,
        choices=REPORT_TYPES
    )

    generated_on = models.DateTimeField(
        auto_now_add=True
    )

    generated_by = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.report_type} - {self.generated_on.strftime('%d-%m-%Y')}"