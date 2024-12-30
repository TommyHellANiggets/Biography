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
    grid_setting = GridSettings.objects.first()
    card_count = grid_setting.card_count if grid_setting else 3
    
    display_order = DisplayCategoryOrder.objects.select_related('category').all()
    categories = Category.objects.all()
    rows = []
    
    recent_articles_ids = set()
    popular_articles_ids = set()

    for item in display_order:
        if item.category_type == 'popular':
            articles = Article.objects.filter(
                category__isnull=False
            ).exclude(
                id__in=popular_articles_ids
            ).order_by('-views')[:card_count]
            
            if articles.exists():
                popular_articles_ids.update(articles.values_list('id', flat=True))
                rows.append({
                    'type': 'popular',
                    'title': 'Популярные',
                    'articles': articles,
                })
                
        elif item.category_type == 'recent' and item.category:
            articles = Article.objects.filter(
                category=item.category
            ).exclude(
                id__in=recent_articles_ids
            ).order_by('-publication_date')[:card_count]
            
            if articles.exists():
                recent_articles_ids.update(articles.values_list('id', flat=True))
                rows.append({
                    'type': 'recent',
                    'title': f"{item.category.name}",
                    'articles': articles,
                })
        else:
            articles = Article.objects.filter(
                category=item.category
            ).order_by('?')[:card_count]
            
            if articles.exists():
                rows.append({
                    'type': 'category',
                    'title': f"{item.category.name}",
                    'articles': articles,
                })

    context = {
        'rows': rows,
        'card_count': card_count,
        'categories': categories,
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
        search_query = Q(title__icontains=query) | Q(tags__name__icontains=query)

        months = {
            'январь': '01', 'февраль': '02', 'март': '03', 'апрель': '04',
            'май': '05', 'июнь': '06', 'июль': '07', 'август': '08',
            'сентябрь': '09', 'октябрь': '10', 'ноябрь': '11', 'декабрь': '12',
            'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04',
            'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08',
            'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'
        }

        words = query.lower().split()
        
        for word in words:
            if word.isdigit() and len(word) == 4:
                year = word
                search_query |= Q(birth_date__year=year) | Q(death_date__year=year)
                
        import re
        date_patterns = [
            r'(\d{1,2})\.(\d{1,2})\.(\d{4})',
            r'(\d{1,2})/(\d{1,2})/(\d{4})'
        ]
        
        for word in words:
            for pattern in date_patterns:
                match = re.match(pattern, word)
                if match:
                    day, month, year = match.groups()
                    day = day.zfill(2)
                    month = month.zfill(2)
                    date_str = f"{year}-{month}-{day}"
                    search_query |= Q(birth_date__contains=date_str) | Q(death_date__contains=date_str)
                    break

        articles = Article.objects.filter(search_query).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results = [{'title': article.title, 'slug': article.slug} for article in articles[:10]]
        return JsonResponse({'results': results})

    grid_setting = GridSettings.objects.first()
    card_count = grid_setting.card_count if grid_setting else 5

    return render(request, 'search_results.html', {
        'articles': articles,
        'query': query,
        'categories': categories,
        'card_count': card_count
    })
