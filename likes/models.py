from django.conf import settings
from django.db import models

from news.models import News


class NewsLikes(models.Model):
    news = models.ForeignKey(News, on_delete=models.SET_NULL, null=True)
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    like = models.BooleanField('Like', default=False)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.liked_by}: {self.news} {self.like}'

    class Meta:
        verbose_name = 'Like news'
        verbose_name_plural = 'Likes news'
