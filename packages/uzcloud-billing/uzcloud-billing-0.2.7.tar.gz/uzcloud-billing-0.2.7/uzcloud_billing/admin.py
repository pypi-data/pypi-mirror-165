from django.contrib import admin

from .models import BillingAccount


@admin.register(BillingAccount)
class BillingAccountAdmin(admin.ModelAdmin):
    list_display = ["user", "account_number", "balance"]
    readonly_fields = ["user", "account_number", "balance"]
