from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Проверка, больше ли 0 число
def validate_positive(value):
    if value < 0:
        raise ValidationError(_("Доходы не могут быть отрицательными"), params={"value":value})