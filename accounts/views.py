from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView

from accounts.forms import RegisterUserForm, LoginUserForm, UpdateUserForm
from accounts.models import User
from accounts.utils import send_email_for_verify


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    # success_url = reverse_lazy('login')
    template_name = 'accounts/register.html'

    def get(self, request):
        context = {'form': RegisterUserForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        context = {'form': form}
        return render(request, self.template_name, context)


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('news_list')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()    # urlsafe_base64_decode() decodes to bytestring
            user = User.objects.get(pk=uid)
        except (TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist,
                ValidationError):
            user = None
        return user


class LoginUser(LoginView):
    form_class = LoginUserForm
    success_url = reverse_lazy('news_list')
    template_name = 'accounts/login.html'


class LogoutUser(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('news_list'))


class Profile(View):

    def get(self, request):
        user = request.user
        return render(request, 'accounts/profile.html', {'user': user})


class ProfileUpdate(UpdateView):

    def get(self, request):
        user = request.user
        default_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        form = UpdateUserForm(default_data)
        return render(request, 'accounts/profile_update.html', {'form': form, 'user': user})

    def post(self, request):
        user = request.user
        default_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return HttpResponseRedirect(reverse('profile'))
        form = UpdateUserForm(default_data)
        return render(request, 'accounts/profile_update.html', {'form': form, 'user': user})
