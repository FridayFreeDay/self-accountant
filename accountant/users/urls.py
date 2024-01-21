from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path

# Параметр для обращения родительского пути через include
app_name = "users"

# Пути для работы с VIEW-хами
urlpatterns = [
    path("register/", views.RegistrationUser.as_view(), name="register"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]