from django.shortcuts import render
from django.contrib.auth.views import LoginView
from base.views import *
from .forms import UserCreateForm
from django.urls.base import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy


# Create your views here.
class LoginView(LoginView):
    template_name = 'userportol/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('custadmin:admin_dashboard')
        else:
            return reverse_lazy('user:dashboard')


class SignupView(BaseCreateView):
    form_class = UserCreateForm
    template_name = "userportol/signup.html"
    success_url = reverse_lazy('user:login')


class DashboardTemplateView(TemplateView):
    template_name = "userportol/shop.html"