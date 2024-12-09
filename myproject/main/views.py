from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Tag, Category
from django.contrib import messages
from .forms import CommentForm


from django.shortcuts import render
from .models import Article, Category

from django.db.models import F

from .models import GridSettings

from .models import DisplayCategoryOrder

from django.shortcuts import render
from .models import Category, Article, DisplayCategoryOrder, GridSettings

def home(request):
    # Загружаем все категории
    categories = Category.objects.all()

    # Получаем настройки отображения категорий
    display_order = DisplayCategoryOrder.objects.select_related('category').all()

    # Получаем настройки сетки (количество карточек в строке)
    grid_setting = GridSettings.objects.first()
    card_count = grid_setting.card_count if grid_setting else 5  # Используем 5 как значение по умолчанию

    # Популярные статьи
    popular_articles = Article.objects.order_by('-views')[:card_count]
    
    # Последние статьи
    recent_articles = Article.objects.order_by('-publication_date')[:card_count]

    # Формируем строки для отображения
    rows = []
    for item in display_order:
        if item.category_type == 'recent':
            rows.append({
                'type': 'recent',
                'title': 'Последние добавленные',
                'articles': recent_articles,
            })
        elif item.category_type == 'popular':
            rows.append({
                'type': 'popular',
                'title': 'Популярные',
                'articles': popular_articles,
            })
        elif item.category_type == 'category' and item.category:
            articles = Article.objects.filter(category=item.category).order_by('-publication_date')[:card_count]
            rows.append({
                'type': 'category',
                'title': item.category.name,
                'articles': articles,
            })

    context = {
        'rows': rows,           # Формируем строки для отображения
        'card_count': card_count,  # Настройки сетки
        'categories': categories,  # Категории для меню
    }
    return render(request, 'main.html', context)



from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import F
from .models import Article, Tag, Category
from .forms import CommentForm


def biography_details(request, slug):
    # Получение статьи по slug
    article = get_object_or_404(Article, slug=slug)

    # Проверка и обновление cookies для учета просмотров
    viewed_articles = request.COOKIES.get('viewed_articles', '').split(',')
    if str(article.id) not in viewed_articles:
        Article.objects.filter(pk=article.pk).update(views=F('views') + 1)
        viewed_articles.append(str(article.id))

    # Получение связанных данных
    tags = Tag.objects.filter(article=article)
    comments = article.comments.all()
    categories = Category.objects.all()

    # Если метод POST, обрабатываем отправку формы
    if request.method == 'POST':
        # Собираем данные вручную из инпутов в шаблоне
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'text': request.POST.get('text'),  # Поле для текста комментария
        }

        form = CommentForm(data)  # Передаем данные в форму
        if form.is_valid():
            # Сохраняем комментарий, связывая его с текущей статьей
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            messages.success(request, "Ваш комментарий успешно опубликован!")
            return redirect('biography_details', slug=article.slug)
        else:
            messages.error(request, "Ошибка при добавлении комментария. Проверьте данные формы.")

    else:
        form = CommentForm()

    response = render(request, 'biography_detail.html', {
        'article': article,
        'tags': tags,
        'comments': comments,
        'form': form,
        'categories': categories,
    })

    # Обновление cookies
    response.set_cookie('viewed_articles', ','.join(viewed_articles), max_age=7 * 24 * 60 * 60)  # Хранить 7 дней

    return response


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import GridSettings

def category_details(request, slug):
    # Получаем текущую категорию
    category = get_object_or_404(Category, slug=slug)
    # Получаем все категории для отображения
    categories = Category.objects.all()
    # Определяем параметр сортировки (по умолчанию - по дате публикации)
    sort_option = request.GET.get('sort', '-publication_date')

    try:
        # Фильтруем статьи по категории и сортируем
        articles = Article.objects.filter(category=category).order_by(sort_option)
    except Exception as e:
        # Если сортировка некорректна, используем стандартный порядок
        print(f"Ошибка сортировки: {e}")
        articles = Article.objects.filter(category=category).order_by('-publication_date')

    # Получаем настройку сетки
    grid_setting = GridSettings.objects.first()  # Берем первую запись настроек
    card_count = grid_setting.card_count if grid_setting else 5  # По умолчанию 5 карточек

    # Рендерим шаблон с категориями, статьями и настройкой сетки
    return render(request, 'catalog_details.html', {
        'category': category,
        'categories': categories,
        'articles': articles,
        'card_count': card_count,
    })


def category(request):
    categories = Category.objects.all()
    articles = Article.objects.all()
    return render(request, 'category.html', {'articles': articles, 'categories': categories})


def biography(request):
    # Загружаем категории
    categories = Category.objects.all()

    # Загружаем 4 популярных статьи (сортировка по просмотрам)
    popular_articles = Article.objects.order_by('-views')[:4]

    # Загружаем 4 последние добавленные статьи (сортировка по дате публикации)
    recent_articles = Article.objects.order_by('-publication_date')[:4]

    # Подготовка строк категорий со статьями
    rows = []
    for category in categories:
        articles = Article.objects.filter(category=category)
        if articles:
            rows.append({
                'category': category,
                'articles': articles
            })

    context = {
        'categories': categories,         # Категории для base.html
        'popular_articles': popular_articles,  # Популярные статьи
        'recent_articles': recent_articles,    # Последние добавленные статьи
        'rows': rows,                     # Строки категорий со статьями
    }
    return render(request, 'biography.html', context)


from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q

def search_articles(request):
    query = request.GET.get('query', '').strip()
    categories = Category.objects.all()
    articles = Article.objects.none()

    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(birth_date__icontains=query) |
            Q(death_date__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Проверка на AJAX-запрос
        results = [{'title': article.title, 'slug': article.slug} for article in articles[:10]]  # Используем slug статьи
        return JsonResponse({'results': results})

    return render(request, 'search_results.html', {'articles': articles, 'query': query, 'categories': categories})
