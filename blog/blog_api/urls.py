from django.urls import path, include
from rest_framework.routers import DefaultRouter
import rest_framework_simplejwt.views as token_views
from . import views

app_name = "blog_api"

view_set_list = [
    {"url": "articles", "view_class": views.ArticleViewSet, "basename": "article"},
    {"url": "users", "view_class": views.UserViewSet, "basename": "user"},
]

router = DefaultRouter()
for view_set in view_set_list:
    router.register(rf'{view_set["url"]}', view_set["view_class"], basename=view_set["basename"])

urlpatterns = [
    # Articles
    path("", include(router.urls)),
    # Users
    path("user_demo_request/", views.UserDemoRequestAPIView.as_view()),
    # JWT
    path('token/', token_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', token_views.TokenRefreshView.as_view(), name='token_refresh'),
]