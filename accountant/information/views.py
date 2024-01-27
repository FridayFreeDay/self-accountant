from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from information.models import Record

from information.forms import RecordForm

# Отлов ошибок страница не найдена
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# Функция для работы с главной страницей сайта
def index(request):
    data = {
        "title": "Главная страница",
    }
    return render(request, "information/index.html", context=data)


# Функция добавления записи о трате
def add_record(request):
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            f["buyer"] = request.user
            Record.objects.create(**f)
            return redirect("users:wallet")
    else:
        form = RecordForm()
    data = {
        "title": "Траты",
        "form": form,
    }
    return render(request, "information/add_record.html", context=data)