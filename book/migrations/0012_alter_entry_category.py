# Generated by Django 4.2.7 on 2023-11-30 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_ledger_month_budget_ledger_year_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.category'),
        ),
    ]