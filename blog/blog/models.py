from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Article(models.Model):
    name = models.fields.CharField(max_length=100, null=False)
    text = models.fields.TextField()
    date_created = models.fields.DateTimeField(default=timezone.now())
    slug = models.SlugField(default="", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Article, self).save(*args, **kwargs)