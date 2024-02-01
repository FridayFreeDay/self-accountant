from datetime import date, datetime
from django.core.paginator import Paginator
from users.forms import FilterForm
from information.models import Record
from django.db.models import Q


# Вывод определённого количества или всех записей/трат пользователя
def records_user(request):
    rec = Record.objects.filter(buyer=request.user).select_related("categories", "buyer")
    return rec


# Функция отображения записей/трат пользователя в виде таблицы постранично, номер страницы передаётся в GET запросе в переменной page
# Возвращает страницу с записями
def pagination_records(request):
    context_list = records_user(request)
    paginator = Paginator(context_list, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


# Функция поиска записей/трат пользователя и суммы трат по GET запросу по переменной q, производится по сумме/описанию/категории 
# Возвращает искомые записи, сумму трат по ним
def search(request):
    query = request.GET.get('q')
    search_list = Record.objects.filter(Q(amount__icontains=query)|
                                        Q(title__icontains=query)|Q(categories__name__icontains=query)).select_related("categories", "buyer")
    expenses = search_expenses(search_list)
    return search_list, expenses


# Функция фильтрации записей/трат пользователя и суммы трат по GET запросу по переменной cats, производится по фильтрации 
# Возвращает искомые записи, сумму трат по ним
def search_filter(request):
    filter_form = FilterForm(request.GET)
    if filter_form.is_valid():
            f = filter_form.cleaned_data
    filter_list = Record.objects.filter(Q(categories__id__in=f["cats"]),
                                        Q(amount__gte=f["start_sum"]) & Q(amount__lte=f["end_sum"]), Q(time_create__date__gte=f["start_date"]) & Q(time_create__date__lte=f["end_date"])).select_related("categories", "buyer")
    expenses = search_expenses(filter_list)
    return filter_list, expenses


# Функция возвращает сумму расходов по записям
def search_expenses(search_list=Record.objects.all()):
    expenses = 0
    for r in search_list:
        expenses += r.amount
    return expenses


# Функция поиска записей/трат пользователя и суммы трат по GET запросу, производится по фильтрации и поиску(распределительная функция)
# Возвращает искомые записи, сумму трат по ним
def search_record_and_expenses(request):
    if request.GET.get("q"):
        record, search_expenses_list = search(request)
    elif request.GET.get("cats"):
        record, search_expenses_list = search_filter(request)
    return record, search_expenses_list