import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(max_length=255, label="Логин", widget=forms.TextInput())
    password = forms.CharField(
        max_length=255, label="Пароль", widget=forms.PasswordInput()
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class RegisterUserForm(UserCreationForm):
    username = username = forms.CharField(
        max_length=255, label="Логин", widget=forms.TextInput()
    )
    password1 = forms.CharField(
        max_length=255, label="Придумайте пароль", widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        max_length=255, label="Подтвердите пароль", widget=forms.PasswordInput()
    )

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
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "E-mail",
        }
        widgets = {
            "email": forms.TextInput(),
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким E-mail уже существует")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=255, label="Логин", disabled=True, widget=forms.TextInput()
    )
    email = forms.CharField(
        max_length=255, label="E-mail", disabled=True, widget=forms.TextInput()
    )
    this_year = datetime.date.today().year
    date_birth = forms.DateField(
        label="Год рождения",
        widget=forms.SelectDateWidget(
            years=tuple(range(this_year - 100, this_year - 5))
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "date_birth", "first_name", "last_name"]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
        }
        widgets = {
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
        }
