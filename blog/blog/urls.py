from django.urls import path
from .views import ArticlesGeneric, ArticleDetailGeneric, create_article

app_name = "blog"

urlpatterns = [
    path('articles/', ArticlesGeneric.as_view(), name="articles"),
    path('article/<int:pk>', ArticleDetailGeneric.as_view(), name="detail_article"),
    path('article-create', create_article, name="create_article")
]