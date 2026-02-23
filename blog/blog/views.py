from datetime import datetime

from django.db.models import Count, Sum, Avg, Min, Max, Q, F
from django.shortcuts import render, redirect
from django.contrib import admin, messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, User
from .forms import ArticleForm


class ArticlesGeneric(LoginRequiredMixin, ListView):
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

class ArticleDetailGeneric(LoginRequiredMixin, DetailView):
    model = Article
    queryset = Article.objects.prefetch_related("watched_users")

    def get_object(self, queryset=None):
        article = super().get_object(queryset=None)
        article.watched_users.add(self.request.user)
        article.save()

        return article


@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article_obj = form.save(commit=False)
            article_obj.user = request.user
            article_obj.save()
            messages.success(request, "Article Create message")
            return redirect('blog:detail_article', pk=article_obj.id)
        else:
            form.add_error(None, "Error with form processing")
    else:
        form = ArticleForm()
    return render(request, 'blog/article_create.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()  # Retrieve the authenticated user
            login(request, user)
            messages.success(request, "Success Login")
            return redirect('blog:articles')
        else:
            form.add_error(None, "Error with Authentication")
    else:
        form = AuthenticationForm()
    return render(request, 'blog/user_login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('auth:login')

def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Success User Registration")
            return redirect('blog:articles')
        else:
            form.add_error(None, "Error with Registration")
    else:
        form = UserCreationForm()
    return render(request, 'blog/user_create.html', {'form': form})













