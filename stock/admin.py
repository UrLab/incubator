from django.contrib import admin

from .models import (
    Category,
    Product,
    TransferTransaction,
    TopupTransaction,
    ProductTransaction,
    MiscTransaction,
    PaymentTransaction,
    FundZone,
    RefundTransaction,
)
import stock.actions as actions

import stock.actions as actions


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


class PaymentTransactionInline(admin.TabularInline):
    model = PaymentTransaction


class RefundTransactionInline(admin.TabularInline):
    model = RefundTransaction


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    search_fields = ("name",)

    actions = (actions.make_active, actions.make_inactive,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = (ProductInline,)


@admin.register(TransferTransaction)
class TransferTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "receiver", "amount", "when")
    search_fields = ("user__username",)


@admin.register(TopupTransaction)
class TopupTransaction(admin.ModelAdmin):
    list_display = ("user", "amount", "topup_type", "when")
    search_fields = ("user__username",)
    list_filter = ("topup_type",)


@admin.register(ProductTransaction)
class ProductTransaction(admin.ModelAdmin):
    list_display = ("user", "price", "product", "when")
    search_fields = ("user__username", "product__name")


@admin.register(MiscTransaction)
class MiscTransaction(admin.ModelAdmin):
    list_display = ("user", "amount", "info", "when")
    search_fields = ("user__username",)


@admin.register(PaymentTransaction)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "zone", "way", "amount", "when")
    search_fields = ("user__username",)
    inlines = (RefundTransactionInline,)

    list_filter = ("user", "zone")

    def get_changeform_initial_data(self, request):
        return {"user": request.user}


@admin.register(FundZone)
class FundZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "method", "balance")
    search_fields = ("name",)
    inlines = (PaymentTransactionInline,)


@admin.register(RefundTransaction)
class RefundTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "amount", "completed")
    actions = [actions.refund_from_bank, actions.refund_from_cash]
