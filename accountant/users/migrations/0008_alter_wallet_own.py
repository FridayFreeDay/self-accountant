# Generated by Django 4.2.9 on 2024-01-27 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_wallet_revenues'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='own',
            field=models.CharField(blank=True, db_index=True, max_length=1000, unique=True, verbose_name='Email владельца'),
        ),
    ]
