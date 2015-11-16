from django.views.generic.edit import CreateView
from users.forms import UserCreationForm
from django.contrib.auth import login

from django.shortcuts import render
from space.djredis import get_redis, space_is_open


def home(request):
    client = get_redis()
    return render(request, "home.html", {
        "space_open": space_is_open(client)
    })



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
