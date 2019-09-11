from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView
from users.mixins import PermissionRequiredMixin
from datetime import datetime
from actstream import action

from .models import Article
from .forms import ArticleForm

def wiki_home(request):
    articles = Article.objects.all()

    return render(request, "wiki_home.html", {
        'all': articles,
    })

class ArticleAddView(PermissionRequiredMixin, CreateView):
    form_class = ArticleForm
    template_name = 'add_article.html'
    permission_required = ''

    def get_initial(self):
        return {
            'creator': self.request.user,
            'created': datetime.now(),
        }

    def form_valid(self, form):
        ret = super(ArticleAddView, self).form_valid(form)
        action.send(self.request.user, verb='a créé', action_object=self.object)

        return ret


class ArticleEditView(PermissionRequiredMixin, UpdateView):
    form_class = ArticleForm
    model = Article
    template_name = 'add_article.html'
    permission_required = ''

    def get_initial(self):
        return {
            'creator': self.request.user,
            'created': datetime.now(),
        }

    def form_valid(self, form):
        ret = super(ArticleEditView, self).form_valid(form)
        action.send(self.request.user, verb='a édité', action_object=self.object)

        return ret

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

class ArticleOldDetailView(ArticleDetailView):
    pass
