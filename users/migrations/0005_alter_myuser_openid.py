# Generated by Django 4.2.7 on 2023-12-15 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_myuser_openid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='openid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]