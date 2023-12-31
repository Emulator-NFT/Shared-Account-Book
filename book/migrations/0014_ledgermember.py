# Generated by Django 4.2.7 on 2023-12-07 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0013_entryimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='LedgerMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('owner', '账本主人'), ('admin', '管理员'), ('member', '普通成员')], default='member', max_length=10)),
                ('nickname', models.CharField(blank=True, max_length=20)),
                ('ledger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='book.ledger')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ledgers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
