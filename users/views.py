from rest_framework import viewsets
# from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from django.contrib import messages

from incubator.settings import BANK_ACCOUNT

from .serializers import UserSerializer
from .models import User
from .forms import UserForm, BalanceForm
from stock.models import Product


def balance(request):
    return render(request, 'balance.html', {
        'account': BANK_ACCOUNT,
        'products': Product.objects.order_by('category'),
    })


def spend(request):
    if request.method == 'POST':
        post = request.POST.copy()
        if 'value' in post:
            post['value'] = post['value'].replace(',', '.')
        form = BalanceForm(post)
        if form.is_valid():
            request.user.balance -= form.cleaned_data['value']
            messages.success(request, 'Vous avez bien dépensé {}€'.format(form.cleaned_data['value']))
            request.user.save()
    return HttpResponseRedirect(reverse('change_balance'))


def top(request):
    if request.method == 'POST':
        post = request.POST.copy()
        if 'value' in post:
            post['value'] = post['value'].replace(',', '.')
        form = BalanceForm(post)
        if form.is_valid():
            request.user.balance += form.cleaned_data['value']
            messages.success(request, 'Vous avez bien rechargé {}€'.format(form.cleaned_data['value']))
            request.user.save()
    return HttpResponseRedirect(reverse('change_balance'))


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
