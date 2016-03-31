from rest_framework import viewsets
# from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
from actstream import action

from .serializers import UserSerializer
from .models import User
from .forms import UserForm, BalanceForm
from .decorators import permission_required
from stock.models import Product


def balance(request):
    return render(request, 'balance.html', {
        'account': settings.BANK_ACCOUNT,
        'products': Product.objects.order_by('category','name'),
        'userslist' : User.objects.all(),
    })


@permission_required('users.change_balance')
def spend(request):
    if request.method == 'POST':
        post = request.POST.copy()
        if 'value' in post:
            post['value'] = post['value'].replace(',', '.')
        form = BalanceForm(post)
        if form.is_valid():
            sumchanged = form.cleaned_data['value']
            name = form.cleaned_data['name']
            request.user.balance -= sumchanged
            action.send(request.user, verb='a depensé {}€ pour le produit {}'.format(sumchanged, name), public=False)
            messages.success(request, 'Vous avez bien dépensé {}€ ({})'.format(sumchanged, name))
            request.user.save()
        else:
            print(form.errors)
            print(form.non_field_errors)
    return HttpResponseRedirect(reverse('change_balance'))


@permission_required('users.change_balance')
def top(request):
    if request.method == 'POST':
        post = request.POST.copy()
        if 'value' in post:
            post['value'] = post['value'].replace(',', '.')
        form = BalanceForm(post)
        if form.is_valid():
            sumchanged = form.cleaned_data['value']
            name = form.cleaned_data['name']
            request.user.balance += sumchanged
            action.send(request.user, verb='a versé {}€ pour la raison {}'.format(sumchanged, name), public=False)
            messages.success(request, 'Vous avez bien rechargé {}€ ({})'.format(sumchanged,name))
            request.user.save()
    return HttpResponseRedirect(reverse('change_balance'))

@permission_required('users.change_balance')
def transfer(request):
    if request.method == 'POST':
        post = request.POST.copy()
        if 'value' in post:
            post['value'] = post['value'].replace(',', '.')
        form = BalanceForm(post)
        if form.is_valid():
            sumchanged = form.cleaned_data['value']
            name = form.cleaned_data['name']
            otheruser = User.objects.get(username=name)
            if otheruser != request.user and sumchanged>0:
                request.user.balance -= sumchanged
                otheruser.balance += sumchanged
                action.send(request.user, verb='a transféré {}€ à {}'.format(sumchanged, name), public=False)
                messages.success(request, 'Vous avez bien transféré {}€ à {}'.format(sumchanged,name))
                request.user.save()
                otheruser.save()
            elif sumchanged <=0:
                messages.error(request, "Vous ne pouvez pas transférer une somme négative")
            elif otheruser != request.user:
                messages.error(request, "Vous ne pouvez pas vous transférer de l'argent à vous même")
    return HttpResponseRedirect(reverse('change_balance'))


def show_pamela(request):
    request.user.hide_pamela = False
    request.user.save()
    return HttpResponseRedirect(reverse('profile'))


def hide_pamela(request):
    request.user.hide_pamela = True
    request.user.save()
    return HttpResponseRedirect(reverse('profile'))


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
