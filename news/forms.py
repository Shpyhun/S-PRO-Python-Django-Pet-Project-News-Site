from django import forms

from news.models import News, Comment


class AddNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
