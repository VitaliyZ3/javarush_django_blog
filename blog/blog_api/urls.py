from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, UserDemoRequestAPIView, UserViewSet

app_name = "blog_api"

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Articles
    path("", include(router.urls)),
    # Users
    path("user_demo_request/", UserDemoRequestAPIView.as_view())
]