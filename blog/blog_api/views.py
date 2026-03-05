from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from .serializers import ArticleSerializer, UserDemoRequestSerializer, UserSerializer
from .paginators import ArticlePaginator
from blog.models import Article, User


class ArticleAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.select_related("user").prefetch_related("approver_users").all()
    serializer_class = ArticleSerializer
    pagination_class = ArticlePaginator
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name", "text"]
    search_fields = ["name", "text", "user__username"]
    ordering_fields = "__all__"
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyObject]

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def send_email_to_demo_user(user_data):
    return f"Email to {user_data["name"]} sent"

class UserDemoRequestAPIView(APIView):

    def post(self, request):
        serializer = UserDemoRequestSerializer(data=request.data)
        if serializer.is_valid():
            res = send_email_to_demo_user(serializer.data)
            return Response({"message": res}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

