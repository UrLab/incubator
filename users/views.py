from rest_framework import viewsets
# from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView

from incubator.settings import BANK_ACCOUNT

from .serializers import UserSerializer
from .models import User
from stock.models import Product


def balance(request):
    return render(request, 'balance.html', {
        'account': BANK_ACCOUNT,
        'products': Product.objects.order_by('category'),
    })


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
