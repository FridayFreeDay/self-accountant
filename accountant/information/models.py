from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


# Таблица категорий
class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name='Название категории')
    subcategory = models.CharField(null=True, max_length=255, verbose_name='Подкатегория', choices=[("1", "Потребности"),
                                                                                                    ("2", "Развлечения"),
                                                                                                    ("3", "Сбережения и инвестиции")])
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"

    # def get_absolute_url(self):
    #     return reverse("category", kwargs={"cat_slug": self.slug})

# Таблица с покупками/тратами
class Record(models.Model):
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    amount = models.DecimalField(max_digits=17,
                                 validators=[MinValueValidator(0.0001, "Сумма должна быть больше 0")],
                                 decimal_places=2, verbose_name="Сумма:")
    title = models.CharField(max_length=255, blank=True, verbose_name="Краткое описание:")
    categories = models.ForeignKey(to="Category", null=True, on_delete=models.SET_NULL, related_name="rec", verbose_name="Категория:")
    buyer = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="buying", verbose_name="Владелец:")

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-time_create"]
        verbose_name= "Запись"
        verbose_name_plural= "Записи"

    # def get_absolute_url(self):
    #     return reverse("record", kwargs={"rec_pk": self.pk})
    