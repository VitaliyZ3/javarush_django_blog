from django.urls import path
from .views import (
    ArticlesGeneric, ArticleDetailGeneric, create_article,
    login_user, logout_user, create_user
)

app_name = "blog"

urlpatterns = [
    path('articles/', ArticlesGeneric.as_view(), name="articles"),
    path('article/<int:pk>', ArticleDetailGeneric.as_view(), name="detail_article"),
    path('article-create', create_article, name="create_article"),
    # path('login', login_user, name="login"),
    path('logout', logout_user, name="logout"),
    path('create_user', create_user, name="create_user")
]