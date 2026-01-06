from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

class Article(models.Model):
    name = models.CharField(max_length=100, null=False)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="ASDA")
    slug = models.SlugField(default="", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class UserFeedback(models.Model):
    username = models.CharField(max_length=128)
    phone = PhoneNumberField()
    email = models.EmailField()
    text = models.TextField()

    def __str__(self):
        return f"Client {self.username} + {self.email}"