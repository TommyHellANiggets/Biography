from django.contrib import admin
from .models import Article, Tag, Comment, Category

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

from django import forms
from django.forms.widgets import DateInput
from datetime import datetime

class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'death_date': forms.DateInput(attrs={'type': 'date'}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        for field_name in ['birth_date', 'death_date', 'publication_date']:
            value = cleaned_data.get(field_name)
            if value and isinstance(value, str):
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
                    try:
                        cleaned_data[field_name] = datetime.strptime(value, fmt).date()
                        break
                    except (ValueError, TypeError):
                        continue
        return cleaned_data


from django.contrib import admin
from .models import Article

import locale

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')  # Установите русский язык для локали

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'category', 'short_publication_date', 'short_birth_date', 'short_death_date')
    list_filter = ('publication_date', 'birth_date', 'death_date', 'category', 'tags')
    search_fields = ('title', 'content')
    ordering = ('-publication_date',)
    prepopulated_fields = {'slug': ('title',)}

    def short_publication_date(self, obj):
        return obj.publication_date.strftime('%d %b %Y') if obj.publication_date else '-'

    def short_birth_date(self, obj):
        return obj.birth_date.strftime('%d %b %Y') if obj.birth_date else '-'

    def short_death_date(self, obj):
        return obj.death_date.strftime('%d %b %Y') if obj.death_date else '-'

    short_publication_date.short_description = "Дата публикации"
    short_birth_date.short_description = "Дата рождения"
    short_death_date.short_description = "Дата смерти"



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article', 'created_at')
    list_filter = ('created_at', 'article')
    search_fields = ('name', 'email', 'text')

from .models import Category, Article, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'photo')  # Отображение имени и приоритета
    list_editable = ('priority',)  # Поле для редактирования прямо в списке
    ordering = ('priority',)  # Сортировка по приоритету
    search_fields = ('name',)  # Поле для поиска
    prepopulated_fields = {"slug": ("name",)}  # Автозаполнение slug


from django.contrib import admin
from .models import GridSettings

@admin.register(GridSettings)
class GridSettingsAdmin(admin.ModelAdmin):
    list_display = ('card_count',)


from django.contrib import admin
from .models import DisplaySettings

@admin.register(DisplaySettings)
class DisplaySettingsAdmin(admin.ModelAdmin):
    list_display = ("show_header", "show_footer")


from django.contrib import admin
from .models import DisplayCategoryOrder

@admin.register(DisplayCategoryOrder)
class DisplayCategoryOrderAdmin(admin.ModelAdmin):
    list_display = ('position', 'category_type', 'category')
    list_display_links = ('category_type',)  # Указываем ссылку на редактирование
    list_editable = ('position',)  # Теперь 'position' можно редактировать
    list_filter = ('category_type',)
    search_fields = ('category__name',)
