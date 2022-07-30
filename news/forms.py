from django import forms

from news.models import News, CommentNews


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'likes']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentNews
        fields = ['text']
