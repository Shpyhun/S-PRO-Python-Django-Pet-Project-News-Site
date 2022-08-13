from django.urls import path
from django.views.generic import TemplateView

from accounts.views import LoginUser, LogoutUser, RegisterUser, EmailVerify, ProfileUpdate, Profile

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('invalid_verify/', TemplateView.as_view(template_name='accounts/invalid_verify.html'), name='invalid_verify'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email',),
    path('confirm_email/', TemplateView.as_view(template_name='accounts/confirm_email.html'), name='confirm_email'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', Profile.as_view(), name='profile'),
    path('profile/update', ProfileUpdate.as_view(), name='profile_update'),
]
