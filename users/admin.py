from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib import auth

from .models import User


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

    list_display = ('username', 'balance', 'email', 'has_key', 'is_superuser',
                    'is_member', 'created', 'groups')
    list_filter = ('balance', 'has_key', 'is_superuser', 'created')
    search_fields = ('username', 'email')

    add_form = auth.forms.UserCreationForm
    form = auth.forms.UserChangeForm
