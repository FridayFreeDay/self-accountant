from typing import Any
from django.contrib.auth import get_user_model
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView 
from django.contrib.auth.views import LoginView
from users.services import pagination_records, records_user, search
from information.models import Record
from users.models import User, Wallet 
from users.forms import AddWalletForm, ChangeWalletForm, LoginUserForm, RegisterUserForm, AuthenticationForm, ProfileUserForm
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
 
# Вывод кошелька пользователя и его трат(по поиску или по страницам), возможность добавлять новые записи и изменять доход
@login_required
def wallet_user(request):
    if request.method == "POST":
        form_modal = ChangeWalletForm(request.POST)
        if form_modal.is_valid():
            f = form_modal.cleaned_data
            Wallet.objects.filter(own=request.user.email).update(revenues=f["revenues"])
    else:
        form_modal = ChangeWalletForm()
    record, count_rec, expenses = pagination_records(request)
    if request.GET.get("q"):
        record = search(request)
    data ={
        "owner": get_object_or_404(User, username=request.user.username),
        "title": "Кошелёк",
        "record": record,
        "count": count_rec,
        "expenses": expenses,
        "modal": form_modal,
    }
    return render(request, "users/wallet.html", data)

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