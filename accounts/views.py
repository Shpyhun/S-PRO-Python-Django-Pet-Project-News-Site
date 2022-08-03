from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView

from accounts.forms import RegisterUserForm, LoginUserForm
from accounts.models import Profile


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('news_list')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('news_list')


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('news_list'))


class ProfileDetail(DetailView):
    model = Profile
    context_object_name = 'profile'
    success_url = reverse_lazy('profile')
    template_name = 'accounts/profile.html'

    def get_queryset(self, profile_slug):
        return Profile.objects.get(slug=profile_slug)

    def profil(request, profile_slug):
        profile = Profile.objects.get(slug=profile_slug)
