from django.conf import settings
from django.db import models

from accounts.models import User
from news.models import News


# class Like(models.Model):
#     news = models.ForeignKey(News, on_delete=models.CASCADE, null=True)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     like = models.BooleanField(default=False)
#     time_create = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.user}: {self.news} {self.like}'
#
#     class Meta:
#         verbose_name = 'Like'
#         verbose_name_plural = 'Likes'
