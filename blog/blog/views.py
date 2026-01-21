from django.views.generic import ListView, DetailView
from .models import Article, User
from datetime import datetime
from django.db.models import Count, Sum, Avg, Min, Max, Q, F

class ArticlesGeneric(ListView):
    model = Article
    paginate_by = 10
    queryset = Article.objects.select_related('user')

    def get_queryset(self):
        if self.request.GET.get("username"):
            queryset = Article.objects.select_related('user').filter(user__username=self.request.GET.get("username"))
        elif self.request.GET.get("user_id"):
            queryset = User.objects.get(id=self.request.GET.get("user_id")).articles_to_approve.all()
        else:
            queryset = super().get_queryset().annotate(number_of_views = Count("watched_users")).values(
                'number_of_views', 'name', 'text', 'pk'
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=None, **kwargs)
        context_data["time_now"] = datetime.now()
        return context_data

class ArticleDetailGeneric(DetailView):
    model = Article
    queryset = Article.objects.prefetch_related("watched_users")
    def get_object(self, queryset=None):
        article = super().get_object(queryset=None)
        article.watched_users.add(self.request.user)
        article.save()

        return article

def get_post_count(request):
    '''
    SELECT * FROM products
    WHERE
        quantity < min_stock
        AND
        quantity = 4
        AND
        name ilike '%laptop%'
    '''
    result = Product.objects.filter(
        Q(quantity__lt=F('min_stock')) &
        Q(quantity=1) &
        Q(name__icontains="laptop")
    )

    '''
    SELECT 
        *, 
        COUNT(posts) as num_posts, 
        AVG (posts__rating) as avg_rating
    FROM Author
        WHERE  
            (num_posts > 5 OR
            avg_rating > 4.0) AND 
            name != admin
    ORDER BY name
        
    '''

    authors_complex_query = Author.objects.annotate(
        num_posts=Count('posts'),  # Анотація: кількість постів
        avg_rating=Avg('posts__rating')  # Анотація: середній рейтинг постів
    ).filter(
        Q(num_posts__gt=5) | Q(avg_rating__gt=4.0)  # Фільтр по анотаціям з АБО
    ).exclude(
        name='admin'
    ).order_by(
        'name'
    )

    authors_complex_query



















