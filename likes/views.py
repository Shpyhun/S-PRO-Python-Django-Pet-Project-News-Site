# from django.http import HttpResponseRedirect
# from django.shortcuts import redirect, get_object_or_404
# from django.urls import reverse
# from django.views import View
#
#
# from news.models import News
#
#
# def LikeView(request, pk):
#     news = get_object_or_404(News, id=request.POST.get('news_slug'))
#     liked = False
#     if news.likes.filter(id=request.user.id).exists():
#         news.likes.remove(request.user)
#         liked = False
#     else:
#         news.likes.add(request.user)
#         liked = True
#     return HttpResponseRedirect(reverse('news_detail', args=[str(pk)]))

# @login_required
# def like_unlike_post(request):
#     user = request.user
#     if request.method == 'POST':
#         post_id = request.POST.get('post_id')
#         post_obj = Post.objects.get(id=post_id)
#         profile = Profile.objects.get(user=user)
#
#         if profile in post_obj.liked.all():
#             post_obj.liked.remove(profile)
#         else:
#             post_obj.liked.add(profile)
#
#         like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
#
#         if not created:
#             if like.value=='Like':
#                 like.value='Unlike'
#             else:
#                 like.value='Like'
#         else:
#             like.value='Like'
#
#             post_obj.save()
#             like.save()

        # data = {
        #     'value': like.value,
        #     'likes': post_obj.liked.all().count()
        # }

        # return JsonResponse(data, safe=False)
    # return redirect('posts:main-post-view')


# class AddLikeView(View):
#     def post(self, request, *args, **kwargs):
#         news_id = int(request.POST.get('news_id'))
#         user_id = int(request.POST.get('user_id'))
#         url_form = int(request.POST.get('url_form'))
#         user_inst = User.objects.get(id=user_id)
#         news_inst = News.objects.get(id=news_id)
#         try:
#             news_like_inst = NewsLikes.objects.get(news=news_inst, liked_by=user_inst)
#         except Exception as e:
#             news_like = NewsLikes(news=news_inst, liked_by=user_inst, like=True)
#             news_like.save()
#         return redirect(url_form)


# class RemoveLikeView(View):
#     def post(self, request, *args, **kwargs):
#         news_likes_id = int(request.POST.get('news_likes_id'))
#         url_form = request.POST.get('url_form')
#         news_like = Like.objects.get(id=news_likes_id)
#         news_like.delete()
#         return redirect(url_form)
