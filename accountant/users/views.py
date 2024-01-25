from typing import Any
from django.contrib.auth import get_user_model
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView 
from django.contrib.auth.views import LoginView
from users.models import User, Wallet 
from users.forms import AddWalletForm, LoginUserForm, RegisterUserForm, AuthenticationForm, ProfileUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


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

# Вывод профиля пользователя и возможность его менять
class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "Профиль"
        return context

    def get_success_url(self) -> str:
        return reverse_lazy("users:profile")

    def get_object(self, queryset=None) -> Model:
        return get_object_or_404(User, username=self.request.user.username)
    
# Вывод кошелька пользователя
class WalletUser(LoginRequiredMixin, DetailView):
    template_name = "users/wallet.html"
    context_object_name = "owner"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "Кошелёк"
        return context
    
    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.request.user.username)


# Создание кошелька пользователя, если его нет
@login_required
def wallet_create(request):
    if request.method == "POST":
        form = AddWalletForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data 
            f["own"] = request.user.email
            f["owner"] = request.user         
            Wallet.objects.create(**f)
            return redirect("users:wallet")
    else:
        form = AddWalletForm()
    data = {
        "name": request.user.first_name,
        "form": form,
        "title": "Создание кошелька",
    }
    return render(request, "users/create_wallet.html", data)

    