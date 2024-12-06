from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Tag, Category
from django.contrib import messages
from .forms import CommentForm


from django.shortcuts import render
from .models import Article, Category

from django.db.models import F

def home(request):
    # Загружаем все категории
    categories = Category.objects.all()

    # Подготовка данных для строк
    rows = []
    for category in categories:
        # Берем до 4 случайных статей из категории
        articles = Article.objects.filter(category=category).order_by('?')[:4]
        if articles:
            rows.append({
                'category': category,
                'articles': articles
            })

    context = {
        'rows': rows,  # Каждая строка: категория и ее статьи
    }
    return render(request, 'main.html', context)



def biography_details(request, slug):
    article = get_object_or_404(Article, slug=slug)

    # Проверяем, есть ли cookie для этой статьи
    viewed_articles = request.COOKIES.get('viewed_articles', '').split(',')

    if str(article.id) not in viewed_articles:
        # Увеличиваем количество просмотров
        Article.objects.filter(pk=article.pk).update(views=F('views') + 1)
        viewed_articles.append(str(article.id))

    tags = Tag.objects.filter(article=article)
    comments = article.comments.all()
    categories = Category.objects.all()
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            messages.success(request, "Ваш комментарий успешно опубликован!")
            return redirect('biography_details', slug=article.slug)

    response = render(request, 'biography_detail.html', {
        'article': article,
        'tags': tags,
        'comments': comments,
        'form': form,
        'categories': categories
    })

    # Обновляем cookies
    response.set_cookie('viewed_articles', ','.join(viewed_articles), max_age=7 * 24 * 60 * 60)  # Хранить 7 дней

    return response




def category_details(request, slug):
    categories = Category.objects.all()
    articles = Article.objects.all()
    return render(request, 'catalog_details.html', {'articles': articles, 'categories': categories})


def category(request):
    categories = Category.objects.all()
    articles = Article.objects.all()
    return render(request, 'category.html', {'articles': articles, 'categories': categories})


def biography(request):
    categories = Category.objects.all()
    articles = Article.objects.all()
    return render(request, 'biography.html', {'articles': articles, 'categories': categories})

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
            Q(tag__name__icontains=query)
        ).distinct()

    return render(request, 'search_results.html', {'articles': articles, 'query': query, 'categories': categories})
