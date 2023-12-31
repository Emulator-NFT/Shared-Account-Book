# Generated by Django 4.2.7 on 2023-12-24 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0021_alter_entry_review_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ledgermember',
            old_name='budget',
            new_name='year_budget',
        ),
        migrations.AddField(
            model_name='ledgermember',
            name='month_budget',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
    ]
