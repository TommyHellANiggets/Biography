from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField("Название", max_length=255, unique=True)
    slug = models.SlugField("Slug", max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField("Название", max_length=255)
    slug = models.SlugField("Slug", max_length=255, unique=True, blank=True)
    photo = models.ImageField("Фотография", upload_to='articles/photos/', blank=True, null=True)
    publication_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    birth_date = models.DateField("Дата рождения", blank=True, null=True)
    death_date = models.DateField("Дата смерти", blank=True, null=True)
    content = HTMLField("Содержание")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-publication_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class Comment(models.Model):
    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Email")
    text = models.TextField("Комментарий")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments', verbose_name="Статья")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']

    def __str__(self):
        return f"Комментарий от {self.name} к статье {self.article.title}"

