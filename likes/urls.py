from django.urls import path

from likes.views import AddLikeView, RemoveLikeView


urlpatterns = [
    path('add_like/', AddLikeView.as_view(), name='add_like'),
    path('remove_like/', RemoveLikeView.as_view(), name='remove_like'),
]
