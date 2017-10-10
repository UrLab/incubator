from rest_framework import viewsets
# from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
from django.db.models import F
from actstream.models import Action
from space.djredis import get_redis
from django.db import transaction


from .serializers import UserSerializer
from .models import User
from .forms import UserForm, SpendForm, TopForm, TransferForm, ProductBuyForm
from .decorators import permission_required
from stock.models import Product, TransferTransaction, TopupTransaction, ProductTransaction, MiscTransaction


def balance(request):
    return render(request, 'balance.html', {
        'account': settings.BANK_ACCOUNT,
        'products': Product.objects.order_by('category', 'name'),
        'topForm': TopForm(),
        'spendForm': SpendForm(),
        'transferForm': TransferForm(),
    })


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


def userdetail(request):
    client = get_redis()
    streampubtosend = []
    streamprivtosend = []
    STREAM_SIZE = 100
    TRANSACTION_NUM = 5 # Number of transactions to be shown on the page
    streamPublic = Action.objects.filter(public=True).prefetch_related('target', 'actor', 'action_object')[:STREAM_SIZE]
    # streamPrivate = Action.objects.filter(public=False).prefetch_related('target', 'actor', 'action_object')[:STREAM_SIZE]

    transfers = list(request.user.transfertransaction_set.all().order_by("-when")[:TRANSACTION_NUM])
    topups = list(request.user.topuptransaction_set.all().order_by("-when")[:TRANSACTION_NUM])
    purchases = list(request.user.producttransaction_set.all().order_by("-when")[:TRANSACTION_NUM])
    misc = list(request.user.misctransaction_set.all().order_by("-when")[:TRANSACTION_NUM])
    # Sort all transactions and keep only the TRANSACTION_NUM most recent
    all_private_transactions = sorted(transfers + topups + purchases + misc, key=lambda x: x.when, reverse=True)[:TRANSACTION_NUM]

    i = 0
    for a in streamPublic:
        if a.actor == request.user:
            streampubtosend.append(a)
            i += 1
            if i == TRANSACTION_NUM:
                break

    return render(request, 'user_detail.html', {
        'stream_pub': streampubtosend,
        'stream_priv': all_private_transactions,
    })


class UserEditView(UpdateView):
    form_class = UserForm
    template_name = 'user_form.html'
    get_success_url = lambda self: reverse('profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'
    slug_field = "username"


class CurrentUserDetailView(UserDetailView):
    def get_object(self):
            return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
