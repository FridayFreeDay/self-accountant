# Generated by Django 4.2.9 on 2024-01-23 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wallet_name',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Название кошелька'),
        ),
    ]
