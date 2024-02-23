from django.contrib import admin
from information.admin import RecordAdmin
from users.models import User, Wallet

# Регистрация моделей в админке
admin.site.register(Wallet)

# Подтаблица в админку User
class WalletAdmin(admin.TabularInline):
    model = Wallet
    # Снаружи
    list_display = ("id", "own")
    # Внутри
    fields = ["own", "revenues"]
    readonly_fields = ["own"]
    can_delete = False

# Регистрация админки User с расширенными настройками для удобства, добавление подтаблицы
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Снаружи
    list_display = ("id", "username", "email")
    list_display_links = ["username", "id"]
    # Внутри
    save_on_top = True
    fields = [("username", "email"), "photo", "date_birth", 
              "is_superuser", "is_staff", "is_active", "groups"]
    inlines = [WalletAdmin, RecordAdmin]

