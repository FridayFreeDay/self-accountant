# Generated by Django 4.2.9 on 2024-02-10 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0007_category_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subcategory',
            field=models.CharField(choices=[('1', 'Потребности'), ('2', 'Развлечения'), ('3', 'Сбережения и инвестиции')], max_length=255, null=True, verbose_name='Подкатегория'),
        ),
    ]