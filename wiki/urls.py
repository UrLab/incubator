from django.conf.urls import url

from .views import (
    wiki_home, ArticleDetailView, ArticleAddView, ArticleEditView, ArticleOldDetailView)

urlpatterns = [
    url(r'^$', wiki_home, name='wiki_home'),
    url(r'^add$', ArticleAddView.as_view(), name='add_article'),
    url(r'^edit/(?P<pk>[0-9]+)$', ArticleEditView.as_view(), name='edit_article'),
    url(r'^(?P<pk>[0-9]+)$', ArticleDetailView.as_view(), name='view_article'),
    url(r'^(?P<pk>[0-9]+)$', ArticleOldDetailView.as_view(), name='view_version')
]
