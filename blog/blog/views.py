from django.views.generic import ListView, DetailView
from .models import Article, User
from datetime import datetime

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
            queryset = super().get_queryset()
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




















