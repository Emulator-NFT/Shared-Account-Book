# Generated by Django 4.2.7 on 2023-12-14 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_myuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='openid',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
