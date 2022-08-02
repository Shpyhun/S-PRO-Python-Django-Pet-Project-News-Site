from django import forms

from news.models import News, Comment


class AddNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
