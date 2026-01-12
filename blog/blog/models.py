from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=False)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="ASDA")
    slug = models.SlugField(default="", null=True, blank=True)
    approver_users = models.ManyToManyField(User, related_name="articles_to_approve")
    watched_users = models.ManyToManyField(User, related_name="watched_users")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug