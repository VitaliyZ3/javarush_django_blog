import django_filters
from blog.models import Article

class ArticleFilter(django_filters.FilterSet):
    name_contains = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )
    user_name = django_filters.CharFilter(
        field_name="user__username",
        lookup_expr="icontains"
    )

    class Meta:
        model = Article
        fields = ["name","user__username"]