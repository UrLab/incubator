from django.urls import path

from wiki import views

urlpatterns = [
    path('', views.wiki_home, name='wiki_home'),
    path('diff', views.diff_article, name='diff_article'),
    path('add', views.ArticleAddView.as_view(), name='add_article'),
    path('edit/<int:pk>', views.ArticleEditView.as_view(), name='edit_article'),
    path('<int:pk>', views.ArticleDetailView.as_view(), name='view_article'),
    path('<int:pl>/old/<int:pk>', views.ArticleOldDetailView.as_view(), name='view_old_version')
]
