from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from users.models import User
from django.db.models import Count
from django.utils import timezone
from django.views.generic import CreateView, UpdateView

from actstream import action as djaction

from users.mixins import PermissionRequiredMixin

from .forms import LeveledBadgeWearForm, BadgeWearForm, ApproveBadgeForm, CreateBadgeForm
from .models import Badge, BadgeWear


class BadgeHomeView(ListView):
    model = Badge
    template_name = 'badges_home.html'
    context_object_name = 'badges'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['approved_badges'] = context['badges'].filter(
            approved=True).annotate(num_wears=Count('badgewear'))

        context['other_badges'] = context['badges'].filter(approved=False)

        return context


class BadgeDetailView(DetailView):
    model = Badge
    template_name = 'badge_detail.html'
    context_object_name = 'badge'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.object.hidden and (not BadgeWear.objects.filter(badge=self.object, user=self.request.user)):
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


class ProposeBadgeView(CreateView):
    form_class = CreateBadgeForm
    model = Badge
    template_name = 'create_badge.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['proposed_by'] = self.request.user
        return initial

    def form_valid(self, form):
        ret = super().form_valid(form)
        djaction.send(self.request.user, verb='a proposé', action_object=self.object)

        return ret


class BadgeApproveView(PermissionRequiredMixin, UpdateView):
    form_class = ApproveBadgeForm
    model = Badge
    template_name = 'approve_badge.html'
    permission_required = 'badges.approve_badge'

    def get_initial(self):
        initial = super().get_initial()
        initial['approved'] = True
        return initial

    def form_valid(self, form):
        ret = super().form_valid(form)
        djaction.send(self.request.user, verb='a approuvé', action_object=self.object)

        return ret


def BadgeWearAddView(request, pk=0):
    if pk == 0:
        return HttpResponseRedirect(reverse('badges_home_view'))

    badge = get_object_or_404(Badge, pk=pk)
    badgeWear = request.user.badgewear_set.filter(badge=badge)

    if not badgeWear or badgeWear[0].level != "MAI":
        return HttpResponseForbidden("Vous n'avez pas \
            les droits pour effectuer cette action")

    if badge.has_level:
        form = LeveledBadgeWearForm(request.POST)
    else:
        form = BadgeWearForm(request.POST)

    if request.method == "POST":
        if badge.has_level:
            form = LeveledBadgeWearForm(request.POST)
        else:
            form = BadgeWearForm(request.POST)

        if form.is_valid():
            badgeWear = BadgeWear(user=form.cleaned_data['user'])
            badgeWear.badge = badge
            badgeWear.level = form.cleaned_data['level'] if badge.has_level else None
            badgeWear.timestamp = timezone.now()
            badgeWear.attributor = request.user
            badgeWear.save()

            if not badge.hidden:
                djaction.send(form.cleaned_data['user'], verb='a recu le badge', action_object=badge)

            return HttpResponseRedirect(
                reverse('badge_view', kwargs={"pk": pk}))
    else:
        return render(
            request, 'add_badgewear.html',
            {'form': form, 'badge': badge}
        )


def promote_user(request, action="", username="", pk=""):
    user = get_object_or_404(User, username=username)
    badge = get_object_or_404(Badge, pk=int(pk))
    badge_wear = get_object_or_404(BadgeWear, badge=badge, user=user)

    if get_object_or_404(BadgeWear, badge=badge, user=request.user).level != "MAI":
        return HttpResponseForbidden(
            "Vous n'avez pas les droits requis pour \
            effectuer cette action")

    if action == "up":
        if badge_wear.level == "DIS":
            badge_wear.level = "MAI"
        elif badge_wear.level == "INI":
            badge_wear.level = "DIS"
        elif badge_wear.level == "RAC":
            badge_wear.level = "INI"
        if not badge.hidden:
            djaction.send(
                user,
                verb='a été promu "{}" pour le badge'.format(badge_wear.get_level_display()),
                action_object=badge)

    elif action == "down":
        if badge_wear.level == "INI":
            badge_wear.level = "RAC"
        elif badge_wear.level == "DIS":
            badge_wear.level = "INI"
        elif badge_wear.level == "MAI":
            badge_wear.level = "DIS"
    else:
        return HttpResponseForbidden(
            "L'action que vous tentez d'effectuer n'existe pas")
    badge_wear.timestamp = timezone.now()
    badge_wear.save()

    return HttpResponseRedirect(reverse("badge_view", args=[pk]))
