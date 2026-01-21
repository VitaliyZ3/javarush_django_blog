from django import forms
from .models import Article
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            "text": forms.Textarea(attrs={"rows": 10}),
        }