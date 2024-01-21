from django.shortcuts import render




menu = [
    {'title': "Главная страница", "url_name": "index"},
    {'title': "Мой кошелёк", "url_name": "wallet"},
    {'title': "Профиль", "url_name": "profile"},
    {'title': "Настройки", "url_name": "configuration"},
    {'title': "Помощь", "url_name": "help"},   
] 



def index(request):
    data = {
        "maintitle": "SELF ACCOUNTANT",
        "title": "Главная страница",
        "menu": menu
    }
    return render(request, "information/index.html", context=data)


