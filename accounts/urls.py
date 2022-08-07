from django.urls import path

from accounts.views import LoginUser, LogoutUser, RegisterUser, profile, profile_update

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    # path('profile/<int:pk>/', ProfileDetail.as_view(), name='profile'),
    path('profile/', profile, name='profile'),
    path('profile/update', profile_update, name='profile_update'),

]
