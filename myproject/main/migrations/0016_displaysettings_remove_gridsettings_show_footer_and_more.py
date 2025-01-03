# Generated by Django 5.1.4 on 2024-12-08 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_gridsettings_show_footer_gridsettings_show_header'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplaySettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_header', models.BooleanField(default=True, verbose_name='Показывать Header')),
                ('show_footer', models.BooleanField(default=True, verbose_name='Показывать Footer')),
            ],
            options={
                'verbose_name': 'Настройка отображения',
                'verbose_name_plural': 'Настройки отображения',
            },
        ),
        migrations.RemoveField(
            model_name='gridsettings',
            name='show_footer',
        ),
        migrations.RemoveField(
            model_name='gridsettings',
            name='show_header',
        ),
    ]
