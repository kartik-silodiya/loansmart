from django.contrib import admin

from .models import LoanApplication


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "monthly_income",
        "loan_amount",
        "credit_history",
        "prediction",
        "confidence",
        "created_at",
    )
    list_filter = ("prediction", "credit_history", "employment_status", "created_at")
    search_fields = ("full_name",)
