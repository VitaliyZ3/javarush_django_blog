from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from django.core.signals import request_finished

from .serializers import (
    ArticleSerializer, UserDemoRequestSerializer,
    UserSerializer, SingleMessageResponseSerializer, SupportTicketRequestSerializer)
from .paginators import ArticlePaginator
from .permissions import IsOwnerOrReadOnlyObject, ArticlePermission
from .mixins import ReadAndCreateModelViewSet
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
    permission_classes = [ArticlePermission]

    def create(self, request, *args, **kwargs):
        """
        Create article

        Mandatory to send name and description for article creation
        """
        return super().create(request, args, kwargs)

class UserViewSet(ReadAndCreateModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def send_email_to_demo_user(user_data):
    return f"Email to {user_data["name"]} sent"

class UserDemoRequestAPIView(APIView):

    @swagger_auto_schema(request_body=UserDemoRequestSerializer, responses={200:SingleMessageResponseSerializer})
    def post(self, request):
        """
        Send link to provided email and subscribe user for future news
        """
        serializer = UserDemoRequestSerializer(data=request.data)
        if serializer.is_valid():
            res = send_email_to_demo_user(serializer.data)
            return Response({"message": res}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    operation_summary="Create ticker for user issue",
    request_body=SupportTicketRequestSerializer,
    responses={200: SingleMessageResponseSerializer}
)
def create_support_ticket(request):
    return Response({"message": "Ticket created"})