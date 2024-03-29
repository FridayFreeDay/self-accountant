from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path

# Параметр для обращения родительского пути через include
app_name = "users"

# Пути для работы с VIEW-хами
urlpatterns = [
    path("register/", views.register, name="register"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("login/", views.login_user, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileUser.as_view(), name="profile"),
    path("statistics/", views.show_stat, name="stat"),
    path("wallet/", views.wallet_user, name="wallet"),
    path("create-wallet/", views.wallet_create, name="create_wallet"),
    path("delete-record/", views.delete_record, name="delete_record"),
]