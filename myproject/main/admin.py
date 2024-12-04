from django.contrib import admin
from .models import Article, Tag, Comment, Category

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publication_date', 'birth_date', 'death_date')
    list_filter = ('publication_date', 'birth_date', 'death_date', 'category', 'tags')
    search_fields = ('title', 'content')
    ordering = ('-publication_date',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article', 'created_at')
    list_filter = ('created_at', 'article')
    search_fields = ('name', 'email', 'text')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  #
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

