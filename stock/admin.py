from django.contrib import admin

from .models import Category, Product, TransferTransaction, TopupTransaction, TopupTransaction, ProductTransaction, MiscTransaction


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (ProductInline,)


@admin.register(TransferTransaction)
class TransferTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'receiver', 'amount', 'when')
    search_filter = ('user__username',)


@admin.register(TopupTransaction)
class TopupTransaction(admin.ModelAdmin):
    list_display = ('user','amount', 'when')
    search_filter = ('user',)


@admin.register(ProductTransaction)
class ProductTransaction(admin.ModelAdmin):
    list_display = ('user','product', 'when')
    search_filter = ('user', 'product__name')


@admin.register(MiscTransaction)
class MiscTransaction(admin.ModelAdmin):
    list_display = ('user','info', 'when')
    search_filter = ('user',)
