from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import View

from likes.models import NewsLikes
from news.models import News


class AddLikeView(View):
    def post(self, request, *args, **kwargs):
        news_id = int(request.POST.get('news_id'))
        user_id = int(request.POST.get('user_id'))
        url_form = int(request.POST.get('url_form'))
        user_inst = User.objects.get(id=user_id)
        news_inst = News.objects.get(id=news_id)
        try:
            news_like_inst = NewsLikes.objects.get(news=news_inst, liked_by=user_inst)
        except Exception as e:
            news_like = NewsLikes(news=news_inst, liked_by=user_inst, like=True)
            news_like.save()
        return redirect(url_form)


class RemoveLikeView(View):
    def post(self, request, *args, **kwargs):
        news_likes_id = int(request.POST.get('news_likes_id'))
        url_form = request.POST.get('url_form')
        news_like = NewsLikes.objects.get(id=news_likes_id)
        news_like.delete()
        return redirect(url_form)
