from django.urls import path
from . import views


# Пути для работы с VIEW-хами
urlpatterns = [
    path("", views.index, name="home"),
    # path("category/<slug:cat_slug>", views.index, name="catogory"),
    # path("record/<int:rec_pk>", views.record, name="record"),
]