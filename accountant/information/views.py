from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from users.models import User
from users.services import records_user, search_expenses
from information.models import Record
from django.contrib.auth.decorators import login_required

from information.forms import RecordForm


# Отлов ошибок страница не найдена
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

# Функция для работы с главной страницей сайта, отображает недавние записи/траты
def index(request):
    if request.user.is_authenticated:
        record = records_user(request)[:5]
        data = {
            "title": "Главная страница",
            "record": record,
            "expenses": search_expenses(),
        }
    else:
        data = {
            "title": "Главная страница",
        }
    return render(request, "information/index.html", context=data)

# Функция добавления записи о трате
@login_required
def add_record(request):
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            f["buyer"] = request.user
            Record.objects.create(**f)
            return redirect(reverse("users:wallet"))
    else:
        form = RecordForm()
    data = {
        "title": "Траты",
        "form": form,
    }
    return render(request, "information/add_record.html", context=data)