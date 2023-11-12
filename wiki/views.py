from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from actstream import action

from .models import Article
from .forms import ArticleForm


def wiki_home(request):
    articles = Article.objects.all().filter(hidden=False, private=False)

    return render(request, "wiki_home.html", {
        'project': articles.filter(category="p"),
        'food': articles.filter(category="n"),
        'miscellaneous': articles.filter(category="d"),
        'objects': articles.filter(category="o"),
        'hackerspace': articles.filter(category="h"),
    })


class ArticleAddView(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    template_name = 'add_article.html'
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.last_modifier = self.request.user.get_username()
        form.instance.hidden = form.instance.hidden or form.instance.private
        ret = super(ArticleAddView, self).form_valid(form)

        if not self.object.hidden:
            action.send(self.request.user, verb='a créé', action_object=self.object)

        return ret


class ArticleEditView(LoginRequiredMixin, UpdateView):
    form_class = ArticleForm
    model = Article
    template_name = 'add_article.html'
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        form.instance.last_modifier = self.request.user.get_username()
        form.instance.last_modified = timezone.now()
        form.instance.hidden = form.instance.hidden or form.instance.private
        ret = super(ArticleEditView, self).form_valid(form)

        if not self.object.hidden:
            action.send(self.request.user, verb='a édité', action_object=self.object)

        return ret


class ArticleDetailView(UserPassesTestMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def test_func(self):
        if self.get_object().private:
            return self.request.user.is_staff
        return True


class ArticleOldDetailView(DetailView):
    model = Article.history.model
    template_name = 'article_old_detail.html'
    context_object_name = 'article'
