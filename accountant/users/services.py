from information.models import Record


# Вывод всех записей трат пользователя в список кортежей
# длины этого списка, суммы расходов
def records_user(request):
    rec = Record.objects.filter(buyer=request.user).select_related("categories")
    record = []
    expenses = 0
    for r in rec:
        expenses += r.amount
        record.append([r.title, r.categories.name, r.amount, r.time_create])
    len_rec = len(record)
    record = enumerate(record, 1)
    return record, len_rec, expenses