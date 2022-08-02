from django import template

from likes.models import NewsLikes

register = template.Library()


@register.simple_tag(takes_context=True)
def is_liked(context, news_id):
    request = context['request']
    try:
        news_likes = NewsLikes.objects.get(news_id=news_id, liked_id=request.user.id).like
    except Exception as e:
        news_likes = False
    return news_likes


@register.simple_tag()
def count_likes(news_id):
    return NewsLikes.objects.filter(news_id=news_id, like=True).count()


@register.simple_tag(takes_context=True)
def news_likes_id(context, news_id):
    request = context['request']
    return NewsLikes.objects.get(news_id=news_id, liked_by=request.user.id).id
