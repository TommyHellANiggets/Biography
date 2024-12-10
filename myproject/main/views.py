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
    sort_option = request.GET.get('sort', '-publication_date')
    
    categories = Category.objects.all()

    display_order = DisplayCategoryOrder.objects.select_related('category').all()

    grid_setting = GridSettings.objects.first()
    card_count = grid_setting.card_count if grid_setting else 5

    try:
        popular_articles = Article.objects.order_by(sort_option)[:card_count]
        recent_articles = Article.objects.order_by(sort_option)[:card_count]
    except Exception as e:
        popular_articles = Article.objects.order_by('-views')[:card_count]
        recent_articles = Article.objects.order_by('-publication_date')[:card_count]

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
            articles = Article.objects.filter(category=item.category).order_by(sort_option)[:card_count]
            rows.append({
                'type': 'category',
                'title': item.category.name,
                'articles': articles,
            })

    context = {
        'rows': rows,
        'card_count': card_count,
        'categories': categories,
        'sort_option': sort_option,
    }
    return render(request, 'main.html', context)



from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import F
from .models import Article, Tag, Category
from .forms import CommentForm


def biography_details(request, slug):
    article = get_object_or_404(Article, slug=slug)

    viewed_articles = request.COOKIES.get('viewed_articles', '').split(',')
    if str(article.id) not in viewed_articles:
        Article.objects.filter(pk=article.pk).update(views=F('views') + 1)
        viewed_articles.append(str(article.id))

    tags = Tag.objects.filter(article=article)
    comments = article.comments.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'text': request.POST.get('text'),
        }

        form = CommentForm(data)
        if form.is_valid():
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

    response.set_cookie('viewed_articles', ','.join(viewed_articles), max_age=7 * 24 * 60 * 60)

    return response


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import GridSettings

from django.shortcuts import render, get_object_or_404
from .models import Category, Article, GridSettings

def category_details(request, slug):
    category = get_object_or_404(Category, slug=slug)

    categories = Category.objects.all()

    sort_option = request.GET.get('sort', '-publication_date')

    try:
        articles = Article.objects.filter(category=category).order_by(sort_option)
    except Exception as e:
        print(f"Ошибка сортировки: {e}")
        articles = Article.objects.filter(category=category).order_by('-publication_date')

    grid_setting = GridSettings.objects.first()
    card_count = grid_setting.card_count if grid_setting else 5

    return render(request, 'category_details.html', {
        'category': category,
        'categories': categories,
        'articles': articles,
        'card_count': card_count,
        'sort_option': sort_option,
    })


def category(request):
    categories = Category.objects.all()
    articles = Article.objects.all()
    return render(request, 'category.html', {'articles': articles, 'categories': categories})


def biography(request):
    categories = Category.objects.all()

    popular_articles = Article.objects.order_by('-views')[:4]

    recent_articles = Article.objects.order_by('-publication_date')[:4]

    rows = []
    for category in categories:
        articles = Article.objects.filter(category=category)
        if articles:
            rows.append({
                'category': category,
                'articles': articles
            })

    context = {
        'categories': categories,
        'popular_articles': popular_articles,
        'recent_articles': recent_articles,
        'rows': rows,
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

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results = [{'title': article.title, 'slug': article.slug} for article in articles[:10]]
        return JsonResponse({'results': results})

    return render(request, 'search_results.html', {'articles': articles, 'query': query, 'categories': categories})
