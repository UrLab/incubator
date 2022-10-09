from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from actstream import action

from .models import Article
from .forms import ArticleForm, DiffForm


def wiki_home(request):
    articles = Article.objects.all().filter(hidden=False)

    return render(request, "wiki_home.html", {
        'project': articles.filter(category="p"),
        'food': articles.filter(category="n"),
        'miscellaneous': articles.filter(category="d"),
        'objects': articles.filter(category="o"),
        'hackerspace': articles.filter(category="h"),
    })


def diff_article(request):
    """Compares two versions of an article."""
    form = DiffForm()

    if request.method == 'POST':
        form_post = DiffForm(request.POST)
        if form_post.is_valid():
            article = form_post.cleaned_data['base_commit']
            old_article = form_post.cleaned_data['comp_commit']
            delta = article.diff_against(old_article, included_fields=['content'])
            return render(request, "diff_article.html", {
                "delta": delta,
                "article": article,
                "old_article": old_article,
                "form": form,
            })

    return render(request, "diff_article.html", {
        "form": form,
    })


class ArticleAddView(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    template_name = 'add_article.html'
    login_url = '/auth/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.last_modifier = self.request.user.get_username()
        ret = super(ArticleAddView, self).form_valid(form)
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
        ret = super(ArticleEditView, self).form_valid(form)
        action.send(self.request.user, verb='a édité', action_object=self.object)

        return ret


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['diff_form'] = DiffForm

        return context

class ArticleOldDetailView(DetailView):
    model = Article.history.model
    template_name = 'article_old_detail.html'
    context_object_name = 'article'
