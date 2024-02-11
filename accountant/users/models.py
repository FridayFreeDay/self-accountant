from django.db import models
from django.contrib.auth.models import AbstractUser

from users.validators import validate_positive

# Переопределение стандартного класса User
class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    email = models.EmailField(verbose_name="Email")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")

# Модель кошелька, связанная с пользователем
class Wallet(models.Model):
    own = models.CharField(max_length=1000, db_index=True,
                           blank=True, unique=True,
                           verbose_name="Email владельца")
    revenues = models.DecimalField(null=True, default=0,
                                   max_digits = 17, decimal_places = 2,
                                   validators=[validate_positive], verbose_name="Доходы:")
    expenses = models.DecimalField(blank=True, null=True,
                                   max_digits = 17, decimal_places = 2,
                                   verbose_name="Расходы:")
    owner=models.OneToOneField(to="User", on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name="wallet", verbose_name="Владелец")

    def __str__(self) -> str:
        return "Кошелёк: " + self.own

    class Meta:
        verbose_name = "Кошелёк"
        verbose_name_plural = "Кошельки"
