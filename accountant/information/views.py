import datetime
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from users.models import Wallet
from information.models import Record
from django.contrib.auth.decorators import login_required

from information.forms import RecordForm


# Отлов ошибок страница не найдена
def page_not_found(request, exception):
    return render(request, "page_not_found.html")

# Функция для работы с главной страницей сайта
def index(request):
    data = {
        "title": "Главная страница",
    }
    return render(request, "information/index.html", context=data)


# Функция добавления записи о трате
@login_required
def add_record(request):
    current_datetime = datetime.datetime.today()
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            f["buyer"] = request.user
            expenses = sum(Record.objects.filter(buyer=request.user,
                                                    time_create__month = current_datetime.month,
                                                    time_create__year = current_datetime.year).values_list("amount", flat=True)) + f["amount"]
            if expenses <= Wallet.objects.get(owner=request.user).revenues:
                cache.delete(f"expenses_{request.user.id}")
                cache.delete(f"record_{request.user.id}")
                cache.delete(f"recomend_record_{request.user.id}")
                cache.set(f"expenses_{request.user.id}", expenses, 60 * 20)
                Record.objects.create(**f)
                return redirect(reverse("users:wallet"))
            else:
                messages.error(request, "Сумма расходов превышает доходы! Измените значение своей доходности.")
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = RecordForm()

    data = {
        "title": "Траты",
        "form": form,
    }
    return render(request, "information/add_record.html", context=data)