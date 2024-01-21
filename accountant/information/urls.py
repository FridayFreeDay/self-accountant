from django.urls import path
from . import views

# Имя для работы родительского пути через include
app_name = "information"

# Пути для работы с VIEW-хами
urlpatterns = [
    path("", views.index, name="home")
]