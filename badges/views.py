from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView
from users.models import User
from django.utils import timezone


from .models import Badge, BadgeWear


class BadgeDetailView(DetailView):
    model = Badge
    template_name = 'badge_detail.html'
    context_object_name = 'badge'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        badge_wear = BadgeWear.objects.filter(badge=self.object)

        context['badge'] = self.object
        context['wearers'] = badge_wear
        user_level = badge_wear.filter(user=self.request.user)
        print(user_level)
        if len(user_level) == 1 and user_level[0].level == "MAI":
            context['is_master'] = True
        else:
            context['is_master'] = False

        return context


class BadgeWearAddView(CreateView):
    form_class = BadgeWear
    template_name = 'add_badgewear.html'

    def get_initial(self):
        return {
            'attributor': self.request.user,
        }


def promote_user(request, action="", username="", pk=""):
    try:
        user = get_object_or_404(User, username=username)
        badge = get_object_or_404(Badge, pk=int(pk))
        badge_wear = get_object_or_404(BadgeWear, badge=badge, user=user)
    except ValueError:
        return HttpResponseBadRequest(
            "La valeur d'ID n'est pas correcte")

    if get_object_or_404(BadgeWear, badge=badge, user=request.user).level != "MAI":
        return HttpResponseForbidden(
            "Vous n'avez pas les droits requis pour \
            effectuer cette action")

    if action == "up":
        if badge_wear.level == "DIS":
            badge_wear.level = "MAI"
        if badge_wear.level == "INI":
            badge_wear.level = "DIS"
    elif action == "down":
        if badge_wear.level == "DIS":
            badge_wear.level = "INI"
        if badge_wear.level == "MAI":
            badge_wear.level = "DIS"
    else:
        return HttpResponseForbidden(
            "L'action que vous tentez d'effectuer n'existe pas")
    badge_wear.timestamp = timezone.now()
    badge_wear.save()

    return HttpResponseRedirect(reverse("badge_view", args=[pk]))
