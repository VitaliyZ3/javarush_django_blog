import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from .filters import ArticleFilter
from blog.models import Article
from blog.forms import ArticleForm

class UserType(DjangoObjectType):

    class Meta:
        model = User
        fields = ["username", "email"]

class ArticleType(DjangoObjectType):
    user = graphene.Field(UserType)

    class Meta:
        model = Article
        fields = "__all__"
        interfaces = (relay.Node,)
        filterset_class = ArticleFilter

    def resolve_user(self, info):
        raise OSError("Something happend with server")


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    article_by_name = graphene.Field(ArticleType, name=graphene.String(required=True))
    articles = DjangoFilterConnectionField(ArticleType)

    def resolve_article_by_name(self, info, name):
        try:
            return Article.objects.filter(name=name).first()
        except Article.DoesNotExist:
            return None

class CreateArticle(graphene.Mutation):
    article = graphene.Field(ArticleType)

    class Arguments:
        name = graphene.String(required=True)
        text = graphene.String()

    def mutate(self, info, **input_data):
        form = ArticleForm(input_data)
        if form.is_valid():
            article_obj = form.save()
            return CreateArticle(article_obj)
        else:
            return form.errors

class Mutation(graphene.ObjectType):
    create_article = CreateArticle.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)