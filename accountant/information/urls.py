from django.urls import path
from . import views


# Пути для работы с VIEW-хами
urlpatterns = [
    path("", views.index, name="home"),
    path("", views.index, name="wallet"),
    path("", views.index, name="home"),
]