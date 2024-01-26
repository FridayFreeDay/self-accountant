from django.contrib import admin
from information.models import Category, Record

# Регистрация в админке таблицы записей/трат
admin.site.register(Record)

# Создание подтаблицы из записей
class RecordAdmin(admin.TabularInline):
    model = Record
    list_display = ["amount", "title", "time_create"]
    readonly_fields = ["time_create"]


# Регистрация в админке таблицы категорий с подтаблицей записей
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Снаружи
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ["name"]} # автозаполнение поля 
    list_display_links = ["name"]
    # Внутри
    save_on_top = True
    fields = ["name", "slug"]
    inlines = [RecordAdmin]