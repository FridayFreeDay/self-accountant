import datetime
from django import forms
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.shortcuts import get_object_or_404

from users.models import Wallet


# Форма авторизации пользователя
class LoginUserForm(AuthenticationForm):
    # Переопределяем стандартный вид выбранных полей
    username = forms.CharField(max_length=255, label="Логин:", widget=forms.TextInput(attrs={"class": "form-class-active"}))
    password = forms.CharField(max_length=255, label="Пароль:", widget=forms.PasswordInput(attrs={"class": "form-class-active"}))

    # Определяем модель пользователя и выбираем поля для отображения в форме
    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


# Форма регистрации пользователя
class RegisterUserForm(UserCreationForm):
    # Переопределяем стандартный вид выбранных полей
    username = forms.CharField(
        max_length=255, label="Логин:", widget=forms.TextInput(attrs={"class": "form-class-active"})
    )
    password1 = forms.CharField(
        max_length=255, label="Придумайте пароль:", widget=forms.PasswordInput(attrs={"class": "form-class-active"})
    )
    password2 = forms.CharField(
        max_length=255, label="Подтвердите пароль:", widget=forms.PasswordInput(attrs={"class": "form-class-active"})
    )

    # Определяем модель пользователя для формы, поля для отображения, переопределяем названия
    # некоторых полей, переопределяем стандартный вид некоторых полей
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        labels = {
            "first_name": "Имя:",
            "last_name": "Фамилия:",
            "email": "E-mail:",
        }
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-class-active"}),
            "first_name": forms.TextInput(attrs={"class": "form-class-active"}),
            "last_name": forms.TextInput(attrs={"class": "form-class-active"}),
        }

    # Проверка на уникальность ПОЧТЫ
    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким E-mail уже существует")
        return email


# Форма личного кабинета пользователя
class ProfileUserForm(forms.ModelForm):
    # Переопределяем стандартный вид выбранных полей и задаём, 
    # что не можем редактировать username и email(disabled=True)
    # определяем поле для выбора года, месяца и дня рождения
    username = forms.CharField(
        max_length=255, label="Логин:", disabled=True, widget=forms.TextInput(attrs={"class": "form-class-none"})
    )
    email = forms.CharField(
        max_length=255, label="E-mail:", disabled=True, widget=forms.TextInput(attrs={"class": "form-class-none"}),
    required=False)
    this_year = datetime.date.today().year
    date_birth = forms.DateField(
        label = "Дата рождения:",
        widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year - 5)), attrs={"class": "form-class-active"}))
    
    # Определяем модель пользователя для формы, выбираем поля для отображения,
    # переименовываем оставшиеся поля для отображения, переопределяем стандартный вид оставшихся полей 
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "date_birth", "first_name", "last_name"]
        labels = {
            "first_name": "Имя:",
            "last_name": "Фамилия:",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-class-active"}),
            "last_name": forms.TextInput(attrs={"class": "form-class-active"}),
        }

# Форма для добавления кошелька пользователю
class AddWalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ["revenues"]
        widgets = {
            "revenues": forms.TextInput(attrs={"class": "form-class-active"}),
            "expenses": forms.TextInput(attrs={"class": "form-class-active"}),
        }

        