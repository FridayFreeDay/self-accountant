# Информация по главному меню всех страниц
menu = [
    {'title': "Главная страница", "url_name": "home"},
    {'title': "Мой кошелёк", "url_name": "users:wallet"},
    {'title': "Статистика", "url_name": "users:stat"},
    # {'title': "Настройки", "url_name": "configuration"},
    # {'title': "Помощь", "url_name": "help"},   
] 

# Регистрация главного меню, чтобы можно было использовать в любом месте проекта с помощью переменной mainmenu
def get_menu_context(request):
    return {"mainmenu": menu}