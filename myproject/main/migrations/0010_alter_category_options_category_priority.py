# Generated by Django 5.1.3 on 2024-12-05 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_delete_rowconfiguration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['priority', 'name'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AddField(
            model_name='category',
            name='priority',
            field=models.PositiveIntegerField(default=0, verbose_name='Приоритет'),
        ),
    ]
