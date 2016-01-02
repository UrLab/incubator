from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib import auth

from .models import User
from space.models import MacAdress


class MacAdressInline(admin.TabularInline):
    model = MacAdress
    extra = 1


class BalanceListFilter(admin.SimpleListFilter):
    title = "Ardoise"
    parameter_name = 'balance'

    def lookups(self, request, model_admin):
        return (
            ('debt', "Moins de -5€"),
            ('neg5', "[-5€, 0€["),
            ('z', '0€'),
            ('pos5', "]0€, 5€]"),
            ('money', "Plus de 5€"),
        )

    def queryset(self, request, queryset):
        if self.value() == 'debt':
            return queryset.filter(balance__lt=-5)
        if self.value() == 'neg5':
            return queryset.filter(
                balance__gte=-5,
                balance__lt=0,
            )

        if self.value() == 'z':
            return queryset.filter(balance=0)

        if self.value() == 'pos5':
            return queryset.filter(
                balance__gt=0,
                balance__lte=5,
            )
        if self.value() == 'money':
            return queryset.filter(balance__gt=5)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def groups(self, user):
        short_name = str
        p = sorted(
            u"<a title='%s'>%s</a>" % (x, short_name(x))
            for x in user.groups.all())
        if user.user_permissions.count():
            p += ['<strong>+</strong>']
        value = ', '.join(p)
        return mark_safe("%s" % value)
    groups.allow_tags = True
    groups.short_description = u'Membre des groupes'

    list_display = ('username', 'balance', 'email', 'has_key', 'is_superuser', 'created', 'groups')
    list_filter = (BalanceListFilter, 'has_key', 'is_superuser', 'created', 'last_login')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    inlines = (MacAdressInline,)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {
            'fields': (('username', 'email'), ('first_name', 'last_name'), ('has_key', 'hide_pamela'), 'balance')
        }),
        (None, {
            'fields': ('password', 'last_login')
        }),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_superuser', 'groups', 'user_permissions')
        }),
    )

    add_form = auth.forms.UserCreationForm
    form = auth.forms.UserChangeForm
