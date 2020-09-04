from django.contrib import admin

from .models import (
    Category, Product, TransferTransaction,
    TopupTransaction, ProductTransaction, MiscTransaction, Payment)


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (ProductInline,)


@admin.register(TransferTransaction)
class TransferTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'receiver', 'amount', 'when')
    search_fields = ('user__username',)


@admin.register(TopupTransaction)
class TopupTransaction(admin.ModelAdmin):
    list_display = ('user', 'amount', 'topup_type', 'when')
    search_fields = ('user__username',)
    list_filter = ('topup_type',)


@admin.register(ProductTransaction)
class ProductTransaction(admin.ModelAdmin):
    list_display = ('user', 'price', 'product', 'when')
    search_fields = ('user__username', 'product__name')


@admin.register(MiscTransaction)
class MiscTransaction(admin.ModelAdmin):
    list_display = ('user', 'amount', 'info', 'when')
    search_fields = ('user__username',)


@admin.register(Payment)
class PaymentAdmin(models.ModelAdmin):
    list_display = ('user', 'amount', 'method', 'when')
    search_fields = ('user__username')

    list_filter = ('method', 'user')