# Generated by Django 5.1.4 on 2024-12-06 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_article_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='categories/photos/', verbose_name='Фотография'),
        ),
    ]