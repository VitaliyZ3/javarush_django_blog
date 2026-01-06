from django.views.generic import ListView, DetailView
from .models import Article, UserFeedback
from datetime import datetime

class ArticlesGeneric(ListView):
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=None, **kwargs)
        context_data["time_now"] = datetime.now()
        return context_data

class ArticleDetailGeneric(DetailView):
    model = Article


def process_feedback(request):
    text = "Hello, my company Tesla got troubles with AI optimizations"
    user_feedback = UserFeedback(
        username="Oleg",
        email="asda@gmail.com",
        phone="+380979132112",
        text=text
    )
    user_feedback.save()
    if generate_and_append_pain_poins(user_feedback):
        user_feedback.refresh_from_db()






















