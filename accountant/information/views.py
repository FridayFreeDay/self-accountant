from django.http import HttpResponseNotFound
from django.shortcuts import render

# Отлов ошибок страница не найдена
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# Функция для работы с главной страницей сайта
def index(request):
    data = {
        "title": "Главная страница",
    }
    return render(request, "information/index.html", context=data)


# def record(request, rec_pk):
#     if request.method == "POST":
#         form = 

