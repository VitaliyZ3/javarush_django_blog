from django.views.generic import ListView, DetailView
from .models import Article, User
from datetime import datetime
from django.db.models import Count, Sum, Avg, Min, Max, Q, F
from .forms import ArticleForm
from django.shortcuts import render, redirect


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

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article_obj = Article(**form.cleaned_data)
            article_obj.user = request.user
            article_obj.save()
            return redirect('blog:detail_article', pk=article_obj.id)
        else:
            form.add_error(None, "Error with form processing")
    else: # if GET method
        form = ArticleForm()
    return render(request, 'blog/article_create.html', {'form': form})
















