from . import views
from django.urls import path

app_name = "users"

urlpatterns = [
    path("register/", views.RegistrationUser.as_view(), name="register"),
]