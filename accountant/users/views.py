from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView 
from django.contrib.auth.views import LoginView 
from users.forms import LoginUserForm, RegisterUserForm, AuthenticationForm, ProfileUserForm

# Меню сайта(временное место хранения)
menu = [
    {'title': "Главная страница", "url_name": "index"},
    {'title': "Мой кошелёк", "url_name": "wallet"},
    {'title': "Профиль", "url_name": "profile"},
    {'title': "Настройки", "url_name": "configuration"},
    {'title': "Помощь", "url_name": "help"},   
] 


# Регистрация пользователя
class RegistrationUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/registration.html"
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("users:login")

# Авторизация пользователя
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}
    success_url = reverse_lazy("index:home")