from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.db.models import F, Count
from django.db import transaction

from users.forms import UserCreationForm

from .serializers import UserSerializer
from .models import User
from .forms import UserForm, SpendForm, TopForm, TransferForm, ProductBuyForm, ChangePasswordForm, AdminChangePasswordForm
from .decorators import permission_required
from stock.models import Product, TransferTransaction, TopupTransaction, ProductTransaction, MiscTransaction


def balance(request):
    favorites = Product.objects.filter(
        producttransaction__user=request.user
    ).exclude(
        active=False
    ).annotate(
        Count("producttransaction")
    ).order_by("-producttransaction__count")[:5]
    return render(request, 'balance.html', {
        'account': settings.BANK_ACCOUNT,
        'products': Product.objects.order_by('category', 'name').exclude(active=False),
        'favorites': favorites,
        'topForm': TopForm(),
        'spendForm': SpendForm(),
        'transferForm': TransferForm(),
    })


@require_POST
def login_view(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        next = request.GET.get("next", "/")
        next = next if next != "" else "/"
        return HttpResponseRedirect(next)
    else:
        messages.error(request, "Aucun compte correspondant à cet identifiant n'a été trouvé")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


@permission_required('users.change_balance')
@require_POST
def buy_product(request):
    if request.method == 'POST':
        form = ProductBuyForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data["product"]
            price = product.price

            with transaction.atomic():
                request.user.balance = F('balance') - price
                request.user.save()

                product_transaction = ProductTransaction(user=request.user, product=product)
                product_transaction.save()

            messages.success(request, 'Vous avez bien dépensé {}€ ({})'.format(price, product.name))
        else:
            messages.error(request, "Erreur, votre dépense n'a pas été enregistrée")

    return HttpResponseRedirect(reverse('change_balance'))


@permission_required('users.change_balance')
@require_POST
def spend(request):
    if request.method == 'POST':
        form = SpendForm(request.POST)
        if form.is_valid():
            sumchanged = form.cleaned_data['value']
            name = form.cleaned_data['name']

            with transaction.atomic():
                request.user.balance = F('balance') - sumchanged
                request.user.save()

                misc_transaction = MiscTransaction(user=request.user, info=name, amount=sumchanged)
                misc_transaction.save()

            messages.success(request, 'Vous avez bien dépensé {}€ ({})'.format(sumchanged, name))
        else:
            messages.error(request, "Erreur, votre dépense n'a pas été enregistrée")

    return HttpResponseRedirect(reverse('change_balance'))


@permission_required('users.change_balance')
@require_POST
def top(request):
    if request.method == 'POST':
        form = TopForm(request.POST)
        if form.is_valid():
            sumchanged = form.cleaned_data['value']

            with transaction.atomic():
                request.user.balance = F('balance') + sumchanged
                request.user.save()

                top_type = form.cleaned_data['location']

                topup_transaction = TopupTransaction(user=request.user, topup_type=top_type, amount=sumchanged)
                topup_transaction.save()

            messages.success(request, 'Vous avez bien rechargé {}€ ({})'.format(sumchanged, top_type))
        else:
            messages.error(request, "Erreur, votre recharge n'a pas été enregistrée")

    return HttpResponseRedirect(reverse('change_balance'))


@staff_member_required
def send_debt_mail(request):
    users = User.objects.filter(balance__lt=0)

    content = """Bonjour {} !
Le Urlab Banking System a détecté une dette de ta part d'un montant de {}€ :O ! N'oublie pas de t'en défaire au plus vite avant que nos avocats ne te tombent dessus !

Note : Il peut s'agir d'une erreur ! Ayant eu un soucis lié à notre base de données dans le courant de l'année 2020, il se peut que ta dette ait déjà été réglée, si c'est le cas, n'hésite pas à nous contacter (contact@urlab.be).
"""

    for user in users:
        message = EmailMultiAlternatives(
            subject="Votre ardoise @UrLab",
            body=content.format(user.username, abs(user.balance)),
            from_email='Trésorerie UrLab <tresorier@urlab.be>',
            to=user.email
        )
        message.send()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@permission_required('users.change_balance')
@require_POST
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            sumchanged = form.cleaned_data['value']
            otheruser = form.cleaned_data['recipient']
            if otheruser != request.user:

                with transaction.atomic():
                    request.user.balance = F('balance') - sumchanged
                    otheruser.balance = F('balance') + sumchanged
                    request.user.save()
                    otheruser.save()

                    transfer_transaction = TransferTransaction(user=request.user, receiver=otheruser, amount=sumchanged)
                    transfer_transaction.save()

                messages.success(
                    request,
                    'Vous avez bien transféré {}€ à {}'.format(sumchanged, otheruser.username)
                )
            else:
                messages.error(request, "Vous ne pouvez pas vous transférer de l'argent à vous même")
        else:
            messages.error(request, "Erreur, votre transfert n'a pas été enregistré")

    return HttpResponseRedirect(reverse('change_balance'))


def show_pamela(request):
    request.user.hide_pamela = False
    request.user.save()
    return HttpResponseRedirect(reverse('profile'))


def hide_pamela(request):
    request.user.hide_pamela = True
    request.user.save()
    return HttpResponseRedirect(reverse('profile'))


def change_passwd(request):
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if user.check_password(form.cleaned_data['old_password']):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                messages.add_message(request, messages.INFO, "Vous devez vous reconnecter pour continuer")
                return HttpResponseRedirect(reverse("login"))
            else:
                messages.add_message(request, messages.ERROR, "Le mot de passe est incorrect")
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            messages.add_message(request, messages.ERROR, "Les mots de passe ne correspondent pas")
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

    context = {
        "form": ChangePasswordForm()
    }
    return render(request, "change_passwd.html", context)


def admin_change_passwd(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = AdminChangePasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            messages.add_message(request, messages.INFO, "Le mot de passe a bien ete modifier")
            return HttpResponseRedirect("/admin")
        else:
            messages.add_message(request, messages.ERROR, "Les mots de passe ne sont pas identiques!")

    context = {
        "form": AdminChangePasswordForm(),
        "user_id": id
    }
    return render(request, "admin_change_passwd.html", context)


class UserEditView(UpdateView):
    form_class = UserForm
    template_name = 'user_form.html'

    def get_success_url(self):
        return reverse('profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        TRANSACTION_NUM = 5  # Number of transactions to be shown on the page

        # Public
        streampubtosend = self.object.actor_actions.filter(public=True)\
            .prefetch_related('target', 'actor', 'action_object')[:TRANSACTION_NUM]

        # Private
        all_private_transactions = []
        if request.user == self.object:
            transfers = list(request.user.transfertransaction_set.all().order_by("-when")[:TRANSACTION_NUM])
            topups = list(request.user.topuptransaction_set.all().order_by("-when")[:TRANSACTION_NUM])
            purchases = list(request.user.producttransaction_set.all().order_by("-when")[:TRANSACTION_NUM])
            misc = list(request.user.misctransaction_set.all().order_by("-when")[:TRANSACTION_NUM])
            # Sort all transactions and keep only the TRANSACTION_NUM most recent
            all_private_transactions = sorted(
                transfers + topups + purchases + misc, key=lambda x: x.when, reverse=True)[:TRANSACTION_NUM]

        context['stream_pub'] = streampubtosend
        context['stream_priv'] = all_private_transactions

        return context


class CurrentUserDetailView(UserDetailView):
    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def get_initial(self):
        initial = super(RegisterView, self).get_initial()
        initial = initial.copy()
        initial['username'] = self.request.GET.get("username")
        return initial

    def form_valid(self, form):
        ret = super(RegisterView, self).form_valid(form)
        user = form.auth_user()
        if user:
            login(self.request, user)
        return ret
