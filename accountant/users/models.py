from django.db import models
from django.contrib.auth.models import AbstractUser

# Переопределение стандартного класса User
class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")