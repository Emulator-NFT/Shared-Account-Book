# Generated by Django 4.2.7 on 2023-12-06 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_alter_entry_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='book.entry')),
            ],
        ),
    ]