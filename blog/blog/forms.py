from django import forms
from .models import Article
from markdownx.widgets import MarkdownxWidget

class ArticleForm(forms.ModelForm):
    text = forms.CharField(
        widget=MarkdownxWidget()
    )

    class Meta:
        model = Article
        fields = ["name", "text"]
        labels = {"name": "Article Name"}

    def clean_text(self):
        text = self.cleaned_data["text"]
        if "django" in text:
            raise forms.ValidationError("You cannot use django word in form")
        else:
            return text

    def save(self, *args, **kwargs):
        print("save method called!")
        return super(ArticleForm, self).save(*args, **kwargs)
