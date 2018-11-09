from django.contrib import admin

from .models import (Category, Product, TransferTransaction, TopupTransaction, ProductTransaction,
                     MiscTransaction, Barcode, StockRefill, ProductRefill, StocktakeLine, Stocktaking)


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


class BarcodeInline(admin.TabularInline):
    model = Barcode
    extra = 1


class ProductRefillInline(admin.TabularInline):
    model = ProductRefill
    extra = 1


class StocktakeLineInline(admin.TabularInline):
    model = StocktakeLine
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_amount')
    search_fields = ('name',)
    inlines = (BarcodeInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (ProductInline,)


@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ("product", "code")
    search_fields = ("product__name", "code")


@admin.register(StockRefill)
class StockRefillAdmin(admin.ModelAdmin):
    list_display = ("user", "when")
    inlines = (ProductRefillInline,)


@admin.register(Stocktaking)
class StocktakingAdmin(admin.ModelAdmin):
    list_display = ("user", "when")
    inlines = (StocktakeLineInline,)


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
    list_display = ('user', 'paid_price', 'product', 'when')
    search_fields = ('user__username', 'product__name')


@admin.register(MiscTransaction)
class MiscTransaction(admin.ModelAdmin):
    list_display = ('user', 'amount', 'info', 'when')
    search_fields = ('user__username',)
