from django.conf import settings

from django.db import models
from django.urls import reverse

from accounts.models import User


class News(models.Model):
    """Model presenting the news"""
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    likes = models.ManyToManyField(User, related_name='news_post')

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news', kwargs={'news_slug': self.slug, 'news_id': self.pk})

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['id', 'title']


class Category(models.Model):
    """Category news model"""
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id', 'name']


class Comment(models.Model):
    """News comment model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True, related_name='comment')
    text = models.TextField(max_length=500)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['user', 'news']
