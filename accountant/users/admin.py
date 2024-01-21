from django.contrib import admin
from users.models import User

# Регистрация моделей в админке
admin.site.register(User)
