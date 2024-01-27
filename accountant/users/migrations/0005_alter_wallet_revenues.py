# Generated by Django 4.2.9 on 2024-01-27 09:59

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_wallet_revenues'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='revenues',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True, validators=[users.validators.validate_positive], verbose_name='Доходы:'),
        ),
    ]
