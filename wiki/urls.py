from django.urls import path

from .views import (
    wiki_home, ArticleDetailView, ArticleAddView, ArticleEditView, ArticleOldDetailView)

urlpatterns = [
    path('', wiki_home, name='wiki_home'),
    path('add', ArticleAddView.as_view(), name='add_article'),
    path('edit/<int:pk>', ArticleEditView.as_view(), name='edit_article'),
    path('<int:pk>', ArticleDetailView.as_view(), name='view_article'),
    path('<int:pl>/old/<int:pk>', ArticleOldDetailView.as_view(), name='view_old_version')
]
