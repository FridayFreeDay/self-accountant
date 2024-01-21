from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path

app_name = "users"

urlpatterns = [
    path("register/", views.RegistrationUser.as_view(), name="register"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]