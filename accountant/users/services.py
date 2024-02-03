from datetime import date, datetime
from django.core.paginator import Paginator
from users.forms import FilterForm
from information.models import Record
from django.db.models import Q
import plotly.express as px



values_list = ("title", "categories__name", "amount", "time_create", "id")

# Вывод определённого всех записей/трат пользователя, графиков по ним 
def records_user(request):
    rec = Record.objects.filter(buyer=request.user).values_list(*values_list)
    page_obj = pagination_records(request, rec)
    ch = chart(rec)
    return page_obj, ch


# Функция отображения записей/трат пользователя в виде таблицы постранично, номер страницы передаётся в GET запросе в переменной page
# Возвращает страницу с записями
def pagination_records(request, context_list):
    # context_list, ch = records_user(request)
    paginator = Paginator(context_list, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


# Функция поиска записей/трат пользователя, суммы трат, графиков по GET запросу по переменной q, производится по сумме/описанию/категории 
# Возвращает искомые записи, сумму трат по ним, графиков по ним
def search(request):
    query = request.GET.get('q')
    search_list = Record.objects.filter(Q(amount__icontains=query)|
                                        Q(title__icontains=query)|Q(categories__name__icontains=query)).values_list(*values_list)
    expenses = search_expenses(search_list)
    page_obj = pagination_records(request, search_list)
    ch = chart(search_list)
    return page_obj, expenses, ch


# Функция фильтрации записей/трат пользователя, суммы трат, графиков по GET запросу по переменной cats, производится по фильтрации 
# Возвращает искомые записи, сумму трат по ним, графиков по ним
def search_filter(request):
    filter_form = FilterForm(request.GET)
    if filter_form.is_valid():
            f = filter_form.cleaned_data
    filter_list = Record.objects.filter(Q(categories__id__in=f["cats"]),
                                        Q(amount__gte=f["start_sum"]) & Q(amount__lte=f["end_sum"]), 
                                        Q(time_create__date__gte=f["start_date"]) & Q(time_create__date__lte=f["end_date"])).values_list(*values_list)
    expenses = search_expenses(filter_list)
    page_obj = pagination_records(request, filter_list)
    ch = chart(filter_list)
    return page_obj, expenses, ch


# Функция возвращает сумму расходов по записям
def search_expenses(search_list=Record.objects.all().values_list(*values_list)):
    expenses = 0
    for e in search_list:
        expenses += e[2]
    return expenses


# Функция поиска записей/трат пользователя, суммы трат, графиков по GET запросу, производится по фильтрации и поиску(распределительная функция)
# Возвращает искомые записи, сумму трат по ним, графики по ним
def search_record_and_expenses(request):
    if request.GET.get("q"):
        record, search_expenses_list, ch = search(request)
    elif request.GET.get("cats"):
        record, search_expenses_list, ch = search_filter(request)
    return record, search_expenses_list, ch


# Функция вывода графиков
def chart(record):
    labels = [r[1] for r in record]
    values = [r[2] for r in record]

    fig = px.pie(names=labels, values=values)
    fig.update_layout(
        legend= dict(
            font=dict(
            size=16
            ),
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="right",
            x=0.9
        ),
        width=500,
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        title={
            "text": "Расходы по категориям",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'family': 'system-ui', 'color': '#003D73'},
        })

    colors = ['#55518E', '#AD567C', '#93BB5D', '#CCB566']

    fig.update_traces(textfont_size=16, marker= dict(colors=colors, line= dict(color='#000000', width=1)))
    chart = fig.to_html(full_html=False)

    fig1 = px.histogram(x=[str(r[3])[:10] for r in record], y=values)
    fig1.update_layout(
        xaxis=dict(
            title='Дата',
            title_font=dict(size=16),
            tickformat='%d.%m.%Y', # Формат даты (день.месяц.год)
            tickmode='linear', # Линейный режим для дат(чтобы по 2 раза не отображалось)
        ),
        yaxis=dict(title='Сумма', title_font=dict(size=16), gridwidth=1), 
        bargap=0.4,
   
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title={
            "text": "Расходы по дате",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'family': 'system-ui', 'color': '#003D73'},
        })
    fig1.update_traces(hovertemplate='Сумма: %{y}')

    chart1 = fig1.to_html(full_html=False)
    
    return chart, chart1
