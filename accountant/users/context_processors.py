# Информация по главному меню всех страниц
header = [
    {'title': "Главная страница", "url_name": "home"},
    {'title': "Мой кошелёк", "url_name": "users:wallet"},
    {'title': "Статистика", "url_name": "users:stat"},
    # {'title': "Настройки", "url_name": "configuration"},
    # {'title': "Помощь", "url_name": "help"},   
] 

footer = [
    {'title': "GitHub", "url_name": "https://github.com/FridayFreeDay/self-accountant"},
    {'title': "Telegram", "url_name": "https://t.me/elementalKorolev"},
    {'title': "Kaggle", "url_name": "https://www.kaggle.com/fridayfreeday"},
]

# Регистрация главного меню, чтобы можно было использовать в любом месте проекта с помощью переменной header
def get_header_context(request):
    return {"header": header}

def get_footer_context(request):
    return {"footer": footer}