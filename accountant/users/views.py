import datetime
from typing import Any
from django.contrib.auth import authenticate, get_user_model, login
from django.db.models.base import Model as Model
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import UpdateView
from information.models import Record
from users.services import activate_email, chart, create_recommendations, records_user, search_record_and_expenses
from users.models import User, Wallet
from users.forms import AddWalletForm, ChangeWalletForm, ChartForm, LoginUserForm, RegisterUserForm, ProfileUserForm, FilterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.tokens import account_activation_token
from django.core.cache import cache


# Активация аккаунта пользователя после подверждения почты
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Спасибо за подтверждение электронной почты, теперь вы можете войти в свою учётную запись.")
        return redirect("users:login")
    else:
        messages.error(request, "Ссылка для активации недействительна! Перейдите на страницу авторизации(войти) и введите свои данные повторно.")

    return redirect("home")


# Регистрация пользователя
def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get("email"))
            return redirect("home")
    else:
        form = RegisterUserForm()

    data = {
        "title": "Регистрация",
        "form": form,
    }
    return render(request, "users/registration.html", data)


# Авторизация пользователя
def login_user(request):
    if request.method == "POST":
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            f = form.cleaned_data
            user = authenticate(request, username=f["username"], password=f["password"])
            if user and user.is_active:
                    login(request, user)
                    return redirect(reverse("home"))
        else:
            try:
                User = get_user_model().objects.get(username=request.POST["username"])
            except:
                messages.error(request, "Такого пользователя не существует, пожалуйста, зарегистрируйтесь.")
                return redirect(reverse_lazy("users:register"))
            else:
                if User and not User.is_active:
                    to_email = User.email
                    activate_email(request, User, to_email)
    else:
        form = LoginUserForm()
    data = {
        "title": "Авторизация",
        "form": form,
    }
    return render(request, "users/login.html", data)



# Вывод профиля пользователя и возможность его менять
class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = "users/profile.html"

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        if request.FILES:
            User.objects.get(pk=self.object.pk).photo.delete()
        return super().post(request, *args, **kwargs)

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
    search_expenses_list = 0
    if request.method == "POST":
        change_form = ChangeWalletForm(request.POST)
        if change_form.is_valid():
            f = change_form.cleaned_data
            if f["revenues"] >= cache.get(f"expenses_{request.user.id}"):
                cache.delete(f"revenues_{request.user.id}")
                Wallet.objects.filter(own=request.user.email).update(revenues=f["revenues"])
            else:
                messages.error(request, "Доход не должен быть меньше суммы расходов.")
    else:
        change_form = ChangeWalletForm()

    if request.GET.get("q") or request.GET.get("cats"):
        record, search_expenses_list = search_record_and_expenses(request)
    else:
        record = records_user(request)

    expenses = cache.get(f"expenses_{request.user.id}")
    if not expenses:
        current_datetime = datetime.datetime.today()
        expenses = sum(Record.objects.filter(buyer=request.user,
                                                time_create__month = current_datetime.month,
                                                time_create__year = current_datetime.year).values_list("amount", flat=True))
        cache.set(f"expenses_{request.user.id}", expenses, 60 * 20)

    data ={
        "title": "Кошелёк",
        "record": record,
        "expenses": expenses,
        "search_expenses": search_expenses_list,
        "change_form": change_form,
        "filter_form": FilterForm(),
        "query_string": request.META['QUERY_STRING'],
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


# Функция удаления записей/трат
@login_required
def delete_record(request):
    del_list = request.POST.getlist("delete")
    if del_list:
        Record.objects.filter(id__in=del_list).delete()
    cache.delete(f"expenses_{request.user.id}")
    cache.delete(f"record_{request.user.id}")
    cache.delete(f"recomend_record_{request.user.id}")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Функция отображения графиков на отдельной странице
@login_required
def show_stat(request):
    wallet = Wallet.objects.filter(owner=request.user).exists()
    if not wallet:
        messages.warning(request, "Для отображения статистики необходимо создать кошелёк.")
        return redirect(reverse("users:wallet"))
    if request.GET:
        form = ChartForm(request.GET)
    else:
        form = ChartForm()
    ch = chart(request)
    recommendations = create_recommendations(request)
    data = {
        "title": "Статистика",
        "form": form,
        "chart": ch[0],
        "chart1": ch[1],
        "msg": ch[2],
        "rec": recommendations,
    }
    return render(request, "users/stat.html", data)