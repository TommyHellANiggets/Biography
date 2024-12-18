# Generated by Django 5.1.4 on 2024-12-10 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_displaycategoryorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='content_markdown',
            field=models.TextField(blank=True, verbose_name='Содержание (Markdown)'),
        ),
        migrations.AddField(
            model_name='article',
            name='editor_type',
            field=models.CharField(choices=[('tiny', 'TinyMCE'), ('markdown', 'Markdown')], default='tiny', max_length=10, verbose_name='Тип редактора'),
        ),
    ]
