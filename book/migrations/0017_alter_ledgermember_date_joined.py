# Generated by Django 4.2.7 on 2023-12-14 03:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0016_remove_ledger_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledgermember',
            name='date_joined',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
