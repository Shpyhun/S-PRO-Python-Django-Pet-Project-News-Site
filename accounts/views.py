from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView

from accounts.forms import RegisterUserForm, LoginUserForm


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
