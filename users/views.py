from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.views.generic.base import TemplateView
from .forms import RegistrationForm
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class UserRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'login.html'


class CustomLogoutView(LogoutView):
    # Customize the logout behavior
    next_page = reverse_lazy('users:logged-out')  # Redirect to the home page for expenses

class CustomLogoutSuccessView(TemplateView):
    template_name = 'logged_out.html'

class HomeView(TemplateView):
    template_name = 'base.html'

class UserProfileView(DetailView, LoginRequiredMixin):
    model = User
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user