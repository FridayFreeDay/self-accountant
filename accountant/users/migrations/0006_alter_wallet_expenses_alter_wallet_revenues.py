# Generated by Django 4.2.9 on 2024-01-27 15:55

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_wallet_revenues'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='expenses',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True, verbose_name='Расходы:'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='revenues',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=17, null=True, validators=[users.validators.validate_positive], verbose_name='Доходы:'),
        ),
    ]