from allauth.account.models import EmailAddress
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView

from accounts.forms import RegisterUserForm, LoginUserForm, UpdateUserForm
from accounts.models import User


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


@login_required
def profile(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})


@login_required
def profile_update(request):
    user = request.user
    if request.method == "POST":
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        default_data = {
            'first_name': user.first_name, 'last_name': user.last_name,
        }
        form = UpdateUserForm(default_data)
    return render(request, 'accounts/profile_update.html', {'form': form, 'user': user})





# class ProfileDetail(DetailView):
#     def get(self, request, pk):
#         user = get_object_or_404(User, pk=pk)
#         form = UpdateUserForm(request, instance=request.user)
#         return render(request, 'accounts/profile.html', {'form': form, 'user': user})
#
#     def post(self, request):
#         form = UpdateUserForm(request, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your profile is updated successfully')
#             return redirect(to='profile')
#         form = UpdateUserForm(instance=request.user)
#         return render(request, 'accounts/profile.html', {'form': form})


# <p>Welcome, {{ user.username }}.
#     {% if not user.profile.account_verified %}
#     (Unverified email.)
#     {% endif %}
# </p>
        # if request.method == 'POST':
        #     user_form = UpdateUserForm(request.POST, instance=request.user)
        #     if user_form.is_valid():
        #         user_form.save()
        #         messages.success(request, 'Your profile is updated successfully')
        #         return redirect(to='users-profile')
        # else:
        #     user_form = UpdateUserForm(instance=request.user)
        # return render(request, 'accounts/profile.html', {'user_form': user_form})