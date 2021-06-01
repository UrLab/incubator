from datetime import datetime

from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib import auth
from django.urls import reverse
from django.utils.html import format_html

from .models import User, Membership
from .utils import current_year
from space.models import MacAdress
from incubator.models import ASBLYear


class MacAdressInline(admin.TabularInline):
    model = MacAdress
    extra = 1


class MembershipInline(admin.TabularInline):
    model = Membership
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

    def change_password(self, user):
        url = reverse("admin_change_passwd", args=(user.id,))
        return format_html(f"<a href='{url}'>Changer le mot de passe</a>")
    change_password.allow_tags = True

    def is_member(self, user):
        """ We suppose each asbl year starts the 15th of june and ends the 14th of june of the next year """

        year = current_year()
        asbl_year, created = ASBLYear.objects.get_or_create(
            start=datetime(year, 6, 15),
            stop=datetime(year + 1, 6, 14)
        )
        membership = Membership.objects.filter(asbl_year=asbl_year, user=user)
        return membership.count() != 0
    is_member.short_description = u'Est membre ASBL'

    def make_member(modeladmin, request, queryset):
        asbl_year = ASBLYear.objects.last()
        for user in queryset.all():
            Membership.objects.create(user=user, asbl_year=asbl_year)
    make_member.short_description = "Rendre membre pour l'année en cours"

    list_display = ('username', 'balance', 'email', 'has_key', 'is_superuser', 'newsletter', 'created', 'groups', 'is_member')
    list_filter = (BalanceListFilter, 'has_key', 'is_superuser', 'created', 'last_login')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    actions = [make_member]

    inlines = (MacAdressInline, MembershipInline)
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('change_password', )

    fieldsets = (
        (None, {
            'fields': (
                ('username', 'email'),
                ('first_name', 'last_name'),
                ('has_key', 'hide_pamela', 'newsletter'),
                'balance'
            )
        }),
        (None, {
            'fields': ('change_password', 'last_login')
        }),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_superuser', 'groups', 'user_permissions')
        }),
    )

    add_form = auth.forms.UserCreationForm
    form = auth.forms.UserChangeForm
