import datetime 
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.forms import FilterForm
from information.models import Record
from django.db.models import Q
import plotly.express as px
from users.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site




def share_by_category(sh1, sh2, sh3):
    msg = []
    if sh1 < 10:
        msg.append(("img/needs.png", "Возможность для открытия своего дела",
                   """У вас в распоряжении есть большое количество свободного капитала, 
                   который при грамотном использовании можно использовать для открытия собственного бизнеса, 
                   что в будущем откроет перед вами ещё больше возможностей.""", sh1))
    elif 10 <= sh1 < 20:
        msg.append(("img/needs.png", "Возможность для повышенных инвестиций",
                   """Благодаря большим доходам и грамотному распоряжению бюджета у вас есть возможность вложить свободные деньги
                   в акции какой либо компании, либо положить деньги на сберегательный счёт, чтобы создать или увеличить 
                   свою \"подушку безопасности\". Не забывайте, что хорошей практикой считается иметь сбережения, которых 
                   хватит на 3 и более месяцев жизни без дохода.""", sh1))
    elif 20 <= sh1 < 30:
        msg.append(("img/needs.png", "Большой свободный капитал",
                   """Грамотное распоряжение внушительными доходами позволяет вам сосредоточиться на инвестициях и сбережениях или 
                   устроить себе приятный вечер, который вы заслужили. Соберитесь с друзьями и отдохните в хорошем месте. 
                   Не забывайте, что хорошей практикой считается иметь сбережения, которых 
                   хватит на 3 и более месяцев жизни без дохода.""", sh1))
    elif 30 <= sh1 < 40:
        msg.append(("img/needs.png", "Свободный капитал",
                   """Вы хорошо распоряжаетесь своими доходами, что позволило вам меньше тратиться на покупки первой необходимости 
                   - это значит, что можно устроить эти деньги в другую сферу, будь то сбережения и инвестиции или отдых с близкими. 
                   Не забывайте, что хорошей практикой считается иметь сбережения, которых 
                   хватит на 3 и более месяцев жизни без дохода.""", sh1))
    elif 40 <= sh1 < 50:
        msg.append(("img/needs.png", "Пониженные обязательные траты",
                   """У вас выдался отличный месяц, поскольку расходы на потребности удаётся держать выше уровня \"золотого 
                   стандарта\", возможно, стоит положить освободившиеся деньги на сберегательный счёт и продолжать работать в том же духе, 
                   чтобы иметь возможность откладывать или инвестировать больше, а также радовать себя развлечениями. 
                   Не забывайте, что хорошей практикой считается иметь сбережения, которых 
                   хватит на 3 и более месяцев жизни без дохода.""", sh1))
    elif 50 <= sh1 < 60:
        msg.append(("img/needs.png", "Повышенные обязательные траты",
                   """Для вас выдался не самый лучший месяц, траты по обязательным категориям превысили показатели \"золотого 
                   стандарта\", вам стоит обратить внимание на обязательные расходы, которые были совершены необдумано и не 
                   лучшим образом - воспользуйтесь графиком расходов по категориям, 
                   также воздержитесь от большого количества трат на развлечения.""", sh1))
    elif 60 <= sh1 < 70:
        msg.append(("img/needs.png", "Режим экономии",
                   """Неудачный месяц, потребности отбирают больше половины всего бюджета, стоит пересмотреть свои расходы 
                   и задуматься о поиске дополнительных источников заработка. Воспользуйтесь графиком расходов по категориям, чтобы 
                   понять, какие траты можно исключить для экономии и стабилизирования бюджета.""", sh1))
    elif 70 <= sh1 < 80:
        msg.append(("img/needs.png", "Режим сильной экономии",
                    """Крайне неудачный месяц, потребности заняли львиную долю бюджета, стоит пересмотреть свои расходы 
                   и задуматься о поиске дополнительных источников заработка. Воспользуйтесь графиком расходов по категориям, чтобы 
                   понять, какие траты можно исключить для ПОВЫШЕННОЙ экономии и стабилизирования бюджета.""", sh1))
    elif 80 <= sh1 < 90:
        msg.append(("img/needs.png", "От зарплаты к зарплате",
                    """Плохой месяц для вас, стоит искать источники дополнительного заработка или задуматься 
                    о смене постоянного места работы в поисках больших доходов. Не используйте без крайней необходимости 
                    \"подушку безопасности\", постарайтесь не терять позитив и ужаться в тратах на развлечения.""", sh1))
    elif sh1 >= 90:
        msg.append(("img/needs.png", "Срочно необходимы дополнительные источники заработка",
                    """Название говорит само за себя, НАЙДИТЕ дополнительный источник заработка или смените работу, 
                    поскольку дальше может стать только хуже, и вам придётся начать использовать \"подушку безопасности\". 
                    Не теряйте позитив, какое-то время придётся сильно ужаться во всех второстепенных расходах.""", sh1))
    if sh2 < 10:
        msg.append(("img/fun.png", "День сурка",
                    """На развлечения тратится очень маленький процент дохода, не забывайте радовать себя, чтобы не выгореть 
                    от монотонного течения дней.""", sh2))
    elif 10 <= sh2 < 20:
        msg.append(("img/fun.png", "Невесёлый месяц",
                    """Выдался не самый весёлый месяц, возможно, вам пришлось закрывать другие расходы, но не забывайте радовать себя 
                    и поддерживать свои хобби, чтобы не заскучать.""", sh2))
    elif 20 <= sh2 < 30:
        msg.append(("img/fun.png", "Серьёзный месяц",
                   """Ваши траты на развлечения чуть ниже \"золотого стандарта\", возможно, месяц выдался загруженным, 
                   и было не так много возможностей для отдыха. Постарайтесь находить больше свободного времени для себя.""", sh2))
    elif 30 <= sh2 < 40:
        msg.append(("img/fun.png", "Весёлый месяц",
                    """Вашему бюджету удавалось достаточно хорошо справляться с расходами на развлечения, 
                    что позволяло вам наслаждаться каждым днем без лишних ограничений. 
                    Помните, что важно уметь радоваться и наслаждаться жизнью, не теряя баланса.""", sh2))
    elif 40 <= sh2 < 50:
        msg.append(("img/fun.png", "Разгульный месяц",
                    """Этот месяц ваш бюджет был несколько предельно расточительным на развлечения, 
                    что могло повлиять на ваши финансовые возможности в будущем. 
                    Помните, что важно обладать дисциплинированностью в планировании расходов, 
                    чтобы избежать финансовых затруднений.""", sh2))
    elif 50 <= sh2 < 60:
        msg.append(("img/fun.png", "Месяц в отрыв",
                    """Ваши траты на развлечения в этом месяце были слишком высокими, 
                    что могло повлечь за собой негативные последствия для вашего финансового благополучия. 
                    Постарайтесь быть более ответственным в планировании своих финансов 
                    и умеренным в трате денег на развлечения.""", sh2))
    elif 60 <= sh2 < 70:
        msg.append(("img/fun.png", "Человек-тусовка",
                    """Ваш месяц был насыщен различными социальными мероприятиями и развлечениями, 
                    которые могли привели к существенным тратам и жизни не по бюджету. 
                    Важно помнить, что не всегда нужно идти на все мероприятия и тратить большие суммы на развлечения, 
                    чтобы быть счастливым. Настоятельно рекомендуется снизить расходы на данную категорию трат.""", sh2))
    elif sh2 >= 70:
        msg.append(("img/fun.png", "Нужен отдых от отдыха",
                    """В этом месяце ваш бюджет был крайне истощён большими тратами на развлечения. 
                    Вам стоит держать себя в руках и стараться не 
                    допускать такого в будущем для сохранения баланса между отдыхом и 
                    работой и возможности отложить деньги на непредвидимые расходы.""", sh2))
    if sh3 == 0:
        msg.append(("img/growth.png", "Без инвестиций",
                    """Этот месяц был достаточно скромным в плане доходов, вам стоит 
                    обратить внимание на возможности для инвестирования, чтобы увеличить свой капитал и 
                    обеспечить более стабильное финансовое будущее.""", sh3))
    elif 0 < sh3 < 10:
        msg.append(("img/growth.png", "Борьба с инфляцией",
                    """Вы активно работали над сохранением покупательной способности своих 
                    средств в условиях взлетающей инфляции. Возможно, стоит рассмотреть дополнительные 
                    инвестиции как способ защиты от влияния инфляции на ваш портфель.""", sh3))
    elif 10 <= sh3 < 20:
        msg.append(("img/growth.png", "Медленный рост",
                    """Ваши инвестиции начинают показывать медленный, но стабильный рост, что говорит о правильно выбранной стратегии. 
                    Продолжайте в том же духе и постепенно увеличивайте свои капиталовложения.""", sh3))
    elif 20 <= sh3 < 30:
        msg.append(("img/growth.png", "Умеренный рост",
                    """Вы наблюдаете умеренный, но устойчивый рост ваших инвестиций. 
                    Это результат тщательного планирования и долгосрочной стратегии. 
                    Продолжайте в том же духе и не теряйте моментов для дополнительных вложений.""", sh3))
    elif 30 <= sh3 < 40:
        msg.append(("img/growth.png", "Ускоренный рост",
                    """Последний месяц оказался довольно успешным для ваших инвестиций, и вы наблюдаете ускоренный рост вашего капитала. 
                    Постарайтесь уделять больше внимания диверсификации портфеля и обязательно проведите анализ рисков.""", sh3))
    elif 40 <= sh3 < 50:
        msg.append(("img/growth.png", "Быстрый рост",
                    """Ваши инвестиции продолжают расти с высокой скоростью, что может свидетельствовать о 
                    успешной стратегии и удачных выборах. 
                    Не забывайте следить за рынком и реагировать на изменения вовремя.""", sh3))
    elif 50 <= sh3 < 60:
        msg.append(("img/growth.png", "Стремительный рост",
                    """Ваши инвестиции демонстрируют стремительный рост. 
                    В данном случае, ваш портфель приносит высокие доходы и возможно показывает выдающиеся результаты. 
                    Важно продолжать балансировать риски и выгоду, 
                    а также оценивать новые возможности для дальнейшего развития и расширения вашего инвестиционного портфеля.""", sh3))
    elif sh3 >= 60:
        msg.append(("img/growth.png", "Инвестиционный человек",
                    """Вы - настоящий инвестиционный человек! 
                    Вы проявляете ум и стремитесь к развитию своего инвестиционного портфеля. 
                    Ваш подход к инвестициям тщательно продуман, и вы принимаете 
                    осознанные решения на основе анализа рынка и данных. 
                    Продолжайте развивать свои навыки и стратегии, чтобы достичь еще большего успеха в мире инвестиций.""", sh3))


    # if 49 < sh1 < 51 and 29 < sh2 < 31 and 19 < sh3 < 21:
    #     msg.append(("Золотой стандарт",
    #                 """Золотой стандарт расходов 50/30/20 - это принцип распределения своих доходов,
    #                 который рекомендует использовать 50% доходов на основные нужды, 30% на желательные расходы и 20% на
    #                 накопления или долгосрочные инвестиции.
    #                 Правильное распределение доходов по этому принципу позволяет поддерживать баланс между
    #                 текущими потребностями, желаниями и обеспечивает финансовую стабильность в будущем.
    #                 Вы придерживаетесь именно этой стратегии.""", (sh1, sh2, sh3)))
    return msg

def create_recommendations(request):
    current_datetime = datetime.datetime.today()
    record = cache.get(f"recomend_record_{request.user.id}")
    if not record:
        record =  Record.objects.filter(buyer=request.user,
                                                                    time_create__month = current_datetime.month,
                                                                    time_create__year = current_datetime.year).values_list("categories__subcategory", "amount")
        cache.set(f"recomend_record_{request.user.id}", record, 60 * 20)
    cat1 = 0
    cat2 = 0
    cat3 = 0
    
    revenues = cache.get(f"revenues_{request.user.id}")
    if not revenues:
        revenues = request.user.wallet.revenues
        cache.set(f"revenues_{request.user.id}", revenues, 60 * 20)

    for rec in record:
        if rec[0] == "1":
            cat1 += rec[1]
        elif rec[0] == "2":
            cat2 += rec[1]
        else:
            cat3 += rec[1]
    if cat1 == cat2 == cat3 == 0:
        message = None
    else:
        share1 = round((cat1 / revenues * 100), 2)
        share2 = round((cat2 / revenues * 100), 2)
        share3 = round((cat3 / revenues * 100), 2)
        message = share_by_category(share1, share2, share3)

    return message


values_list = ("title", "categories__name", "amount", "time_create", "id")

# Функция отправки сообщения на почту для активации аккаунта через подтверждение по почте
def activate_email(request, user, to_email):
    mail_subject = "Активация учётной записи"
    message = render_to_string("users/activate_account.html", {
        "user": user.username,
        "domain": get_current_site(request).domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
        "protocol": "https" if request.is_secure() else "http"
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Уважаемый(-ая) {user}, пожалуйста, перейдите по указанной почте {to_email} и подвердите регистрацию.")
    else:
        messages.error(request, f"Проблемы при отправке письма на почту {to_email}, проверьте корректность данных.")


# Вывод всех записей/трат пользователя
def records_user(request):
    current_datetime = datetime.datetime.today()
    rec = cache.get(f"record_{request.user.id}")
    if not rec:
        rec = Record.objects.filter(buyer=request.user,
                                                            time_create__month = current_datetime.month,
                                                            time_create__year = current_datetime.year).values_list(*values_list)
        cache.set(f"record_{request.user.id}", rec, 60 * 20)
    page_obj = pagination_records(request, rec)
    return page_obj


# Функция отображения записей/трат пользователя в виде таблицы постранично, номер страницы передаётся в GET запросе в переменной page
# Возвращает страницу с записями
def pagination_records(request, context_list):
    paginator = Paginator(context_list, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


# Функция поиска записей/трат пользователя, суммы трат по GET запросу по переменной q, производится по сумме/описанию/категории
# Возвращает искомые записи, сумму трат по ним
def search(request):
    query = request.GET.get('q')
    search_list = Record.objects.filter(Q(buyer=request.user), Q(amount__icontains=query)|
                                        Q(title__icontains=query)|Q(categories__name__icontains=query)).values_list(*values_list)
    expenses = search_expenses(search_list)
    page_obj = pagination_records(request, search_list)
    return page_obj, expenses


# Функция фильтрации записей/трат пользователя, суммы трат по GET запросу по переменной cats, производится по фильтрации
# Возвращает искомые записи, сумму трат по ним
def search_filter(request):
    filter_form = FilterForm(request.GET)
    if filter_form.is_valid():
            f = filter_form.cleaned_data
    filter_list = Record.objects.filter(Q(buyer=request.user), Q(categories__id__in=f["cats"]),
                                        Q(amount__gte=f["start_sum"]) & Q(amount__lte=f["end_sum"]),
                                        Q(time_create__date__gte=f["start_date"]) & Q(time_create__date__lte=f["end_date"])).values_list(*values_list)
    expenses = search_expenses(filter_list)
    page_obj = pagination_records(request, filter_list)
    return page_obj, expenses


# Функция возвращает сумму расходов по записям
def search_expenses(search_list):
    expenses = 0
    for e in search_list:
        expenses += e[2]
    return expenses


# Функция поиска записей/трат пользователя, суммы трат по GET запросу, производится по фильтрации и поиску(распределительная функция)
# Возвращает искомые записи, сумму трат по ним
def search_record_and_expenses(request):
    if request.GET.get("q"):
        record, search_expenses_list = search(request)
    elif request.GET.get("cats"):
        record, search_expenses_list = search_filter(request)
    return record, search_expenses_list


# Функция вывода графиков
def chart(request):
    msg = "Выберите дату"
    labels = [None]
    values = [None]
    x = [None]
    if request.GET:
        start = request.GET.get("start")
        end = request.GET.get("end")
        record = Record.objects.filter(Q(buyer=request.user),
                                                                    Q(time_create__date__range=(start, end))).values_list(*values_list)
        if record:
            pass
        else:
            current_datetime = datetime.datetime.today()
            record = Record.objects.filter(buyer=request.user,
                                                                        time_create__month = current_datetime.month,
                                                                        time_create__year = current_datetime.year).values_list(*values_list)
            msg = "Нет записей в данном промежутке"
    else:
        current_datetime = datetime.datetime.today()
        record = Record.objects.filter(buyer=request.user,
                                                                    time_create__month = current_datetime.month,
                                                                    time_create__year = current_datetime.year).values_list(*values_list)

    if record:
        labels = [r[1] for r in record]
        values = [r[2] for r in record]
        x = [str(r[3])[:10] for r in record]

    fig = px.pie(names=labels, values=values)
    fig.update_layout(
        legend= dict(
            font=dict(
            size=14,
            color="black",
            ),
            orientation="h",
            yanchor="bottom",
            y=-0.6,
            xanchor="right",
            x=0.6
        ),
        width=500,
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        title={
            "text": "Расходы по категориям",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24, 'family': 'system-ui', 'color': 'black'},
        })

    colors = ['#d0e6dc', '#e6fff5', '#b8ccc4', '#8a9993', '#7d8b85', '#9fb1a9', '#717d78', '#424947']

    fig.update_traces(textfont_size=16, 
                      marker= dict(colors=colors, line= dict(color='#000000', width=1)),
                      hovertemplate='Категория: %{label}<br>Сумма: %{value}')
    chart = fig.to_html(full_html=False, config = {'displayModeBar': False})

    fig1 = px.bar(x=x, y=values, color_discrete_sequence=['#d0e6dc'])
    fig1.update_layout(
        xaxis=dict(
            title='Дата',
            title_font=dict(size=18, color="black"),
            tickformat='%d.%m.%Y', # Формат даты (день.месяц.год)
            tickmode='linear', # Линейный режим для дат(чтобы по 2 раза не отображалось)
            tickfont=dict(color="black")
        ),
        yaxis=dict(
            title='Сумма',
            title_font=dict(size=18, color="black"),
            tickfont=dict(color="black"),
            gridwidth=1),

        bargap=0.5,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title={
            "text": "Расходы по дате",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24, 'family': 'system-ui', 'color': 'black'},
        })
    fig1.update_traces(hovertemplate='Сумма: %{y}')

    chart1 = fig1.to_html(full_html=False, config = {'displayModeBar': False})

    return chart, chart1, msg
