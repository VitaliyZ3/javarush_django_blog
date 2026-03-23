import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.decorators import login_required
from blog.models import Article

class ArticleType(DjangoObjectType):

    class Meta:
        model = Article
        fields = "__all__"

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    article_by_name = graphene.Field(ArticleType, name=graphene.String(required=True))


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

    def mutate(self, info, name, text = None):
        article_obj = Article.objects.create(name=name,text=text)
        return CreateArticle(article_obj)

class Mutation(graphene.ObjectType):
    create_book = CreateArticle.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)