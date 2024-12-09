from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField


from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField("Название", max_length=255, unique=True)
    slug = models.SlugField("Slug", max_length=255, unique=True, blank=True)
    photo = models.ImageField("Фотография", upload_to='categories/photos/', blank=True, null=True)  # Поле для фото
    priority = models.PositiveIntegerField("Приоритет", default=0)  # Поле для управления порядком

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['priority', 'name']  # Сортировка по приоритету, затем по названию

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


from django.db.models import F

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
    views = models.PositiveIntegerField("Просмотры", default=0)

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


from django.db import models

class GridSettings(models.Model):
    CARD_COUNT_CHOICES = [
        (3, '3 карточки в строку'),
        (4, '4 карточки в строку'),
        (5, '5 карточек в строку'),
        (6, '6 карточек в строку'),
    ]
    card_count = models.IntegerField(choices=CARD_COUNT_CHOICES, default=5, verbose_name="Количество карточек в строку")

    class Meta:
        verbose_name = "Настройка сетки"
        verbose_name_plural = "Настройки сетки"

    def __str__(self):
        return f"{self.card_count} карточек в строку"


from django.db import models

class DisplaySettings(models.Model):
    show_header = models.BooleanField("Показывать Header", default=True)
    show_footer = models.BooleanField("Показывать Footer", default=True)

    def __str__(self):
        return "Настройки отображения Header и Footer"

    class Meta:
        verbose_name = "Настройка отображения"
        verbose_name_plural = "Настройки отображения"


from django.db import models

class DisplayCategoryOrder(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('recent', 'Последние добавленные'),
        ('popular', 'Популярные'),
        ('category', 'Категория'),
    ]

    category_type = models.CharField(
        max_length=20,
        choices=CATEGORY_TYPE_CHOICES,
        verbose_name="Тип отображения",
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Категория (если выбрана)"
    )
    position = models.PositiveIntegerField("Позиция", default=0)

    class Meta:
        verbose_name = "Отображение категорий"
        verbose_name_plural = "Отображение категорий"
        ordering = ['position']

    def __str__(self):
        if self.category_type == 'category' and self.category:
            return f"{self.position}. {self.category.name}"
        return f"{self.position}. {dict(self.CATEGORY_TYPE_CHOICES).get(self.category_type)}"
