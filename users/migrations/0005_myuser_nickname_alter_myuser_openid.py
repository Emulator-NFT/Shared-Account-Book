# Generated by Django 4.2.7 on 2023-12-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_myuser_openid'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='nickname',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='openid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]