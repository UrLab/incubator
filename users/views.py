from rest_framework import viewsets
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView

from incubator.settings import BANK_ACCOUNT

from .serializers import UserSerializer
from .models import User
from .forms import BalanceForm


def change_balance(request):
    if request.method == 'POST':
        form = BalanceForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('profile'))

    else:
        form = BalanceForm(instance=request.user)

    return render(request, 'balance.html', {'form': form, 'account': BANK_ACCOUNT})


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
