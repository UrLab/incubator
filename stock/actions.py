from django.contrib import admin


@admin.action(description="Marquer les produits sélectionnés comme actifs")
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


@admin.action(description="Marquer les produits sélectionnés comme inactifs")
def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)
