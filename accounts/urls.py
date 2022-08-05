from django.urls import path

from accounts.views import LoginUser, LogoutUser, RegisterUser, ProfileDetail

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/<int:profile_id>/', ProfileDetail.as_view(), name='profile')
]
