from django import forms
from django.core.exceptions import ValidationError

from news.models import News, Comment


class AddNewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'not selected'

    class Meta:
        model = News
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'category']
        widgets = {
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 200:
            raise ValidationError('Length is less than 200 characters')
        return content


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
