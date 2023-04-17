from django.contrib import admin
from stock.models import FundZone


@admin.action(description="Refund the user from the bank zone")
def refund_from_bank(modeladmin, request, queryset):
    fund_zone = FundZone.objects.get(method="BANK")
    for obj in queryset:
        obj.refund(fund_zone, request.user)


@admin.action(description="Refund the user from the cash zone")
def refund_from_cash(modeladmin, request, queryset):
    fund_zone = FundZone.objects.get(method="CASH")
    for obj in queryset:
        obj.refund(fund_zone, request.user)


@admin.action(description="Marquer les produits sélectionnés comme actifs")
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


@admin.action(description="Marquer les produits sélectionnés comme inactifs")
def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)
