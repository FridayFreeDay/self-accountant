from django.core.paginator import Paginator
from information.models import Record
from django.db.models import Q


# Вывод определённого количества или всех записей/трат пользователя, их количества, суммы расходов
def records_user(request, count=Record.objects.all().count()):
    rec = Record.objects.filter(buyer=request.user).select_related("categories")[:count]
    expenses = 0
    count_rec = 0
    for r in rec:
        expenses += r.amount
        count_rec += 1
    return rec, count_rec, expenses

# Функция отображения записей/трат пользователя в виде таблицы постранично, номер страницы передаётся в GET запросе в переменной page
# Возвращает страницу с записями, количество всех записей, суммы трат по всем записям
def pagination_records(request):
    context_list, count_rec, expenses = records_user(request)
    paginator = Paginator(context_list, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj, count_rec, expenses

# Функция поиска записей/трат пользователя по GET запросу по переменной q, производится по сумме/описанию/категории 
# Возвращает искомые записи
def search(request):
    query = request.GET.get('q')
    search_list = Record.objects.filter(Q(amount__icontains=query)|
                                        Q(title__icontains=query)|Q(categories__name__icontains=query)).select_related("categories", "buyer")
    return search_list