# Generated by Django 4.2.7 on 2023-11-07 11:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_entry_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
