from django import forms

from information.models import Category, Record


# Форма создания записи о тратах
class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ["title", "amount", "categories"]
        widgets = {
            "title": forms.Textarea(attrs={"class": "form-class-active", "cols": "30", "rows": "2", 'style':'resize:none;'}),
            "amount": forms.TextInput(attrs={"class": "form-class-active"}),
            "categories": forms.Select(attrs={"class": "form-class-active"}),
        }

# Форма фильтрации записей/трат
class FilterForm(forms.Form):
    date = forms.CharField(widget=forms.SelectDateWidget(), label="Дата", required=False)
    cats = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория")
    summ = forms.DecimalField(label="Сумма", required=False)
