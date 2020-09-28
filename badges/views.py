from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from users.models import User
from django.db.models import Count
from django.utils import timezone

from .forms import BadgeWearForm
from .models import Badge, BadgeWear


class BadgeHomeView(ListView):
    model = Badge
    template_name = 'badges_home.html'
    context_object_name = 'badges'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['badges'] = self.object_list.annotate(num_wears=Count('badgewear'))

        return context


class BadgeDetailView(DetailView):
    model = Badge
    template_name = 'badge_detail.html'
    context_object_name = 'badge'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if not BadgeWear.objects.filter(badge=self.object, user=self.request.user):
            context['authorized'] = False
            return context

        context['authorized'] = True

        badge_wear = BadgeWear.objects.filter(badge=self.object)

        context['badge'] = self.object
        context['wearers'] = badge_wear
        user_level = badge_wear.filter(user=self.request.user)
        if len(user_level) == 1 and user_level[0].level == "MAI":
            context['is_master'] = True
        else:
            context['is_master'] = False

        return context


def BadgeWearAddView(request, pk=0):
    if pk == 0:
        return HttpResponseRedirect(reverse('badges_home_view'))

    form = BadgeWearForm()
    badge = get_object_or_404(Badge, pk=pk)
    badgeWear = request.user.badgewear_set.filter(badge=badge)

    if not badgeWear or badgeWear[0].level != "MAI":
        return HttpResponseForbidden("Vous n'avez pas \
            les droits pour effectuer cette action")

    if request.method == "POST":
        form = BadgeWearForm(request.POST)

        if form.is_valid():

            badgeWear = BadgeWear(user=form.cleaned_data['user'])
            badgeWear.badge = badge
            badgeWear.level = form.cleaned_data['level']
            badgeWear.action_counter = 0
            badgeWear.timestamp = timezone.now()
            badgeWear.attributor = request.user
            badgeWear.save()

            return HttpResponseRedirect(
                reverse('badge_view', kwargs={"pk": pk}))
    else:
        return render(
            request, 'add_badgewear.html',
            {'form': form, 'badge': badge}
        )


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
        if badge_wear.level == "RAC":
            badge_wear.level = "INI"
    elif action == "down":
        if badge_wear.level == "INI":
            badge_wear.level = "RAC"
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
