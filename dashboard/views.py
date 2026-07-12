from django.shortcuts import render

from assets.models import Asset
from accounts.models import CustomUser
from core.models import Department
from maintenance.models import MaintenanceRecord
from audit.models import AuditLog


def dashboard(request):

    context = {

        "total_assets": Asset.objects.count(),

        "available_assets":
            Asset.objects.filter(status="Available").count(),

        "allocated_assets":
            Asset.objects.filter(status="Allocated").count(),

        "maintenance_assets":
            Asset.objects.filter(status="Maintenance").count(),

        "departments":
            Department.objects.count(),

        "employees":
            CustomUser.objects.count(),

        "asset_value":
            sum(asset.current_value for asset in Asset.objects.all()),

        "recent_maintenance":
            MaintenanceRecord.objects.order_by("-maintenance_date")[:5],

        "recent_logs":
            AuditLog.objects.order_by("-timestamp")[:5],

    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )