from django.views.generic import ListView, DetailView
from .models import Article
from datetime import datetime

class ArticlesGeneric(ListView):
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=None, **kwargs)
        context_data["time_now"] = datetime.now().strftime("%I:%M%p on %B %d, %Y")
        return context_data

    def get_queryset(self):
        return Article.objects.filter(name__icontains='SQL')

class ArticleDetailGeneric(DetailView):
    model = Article























