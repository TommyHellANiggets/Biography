from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Tag, Category
from django.contrib import messages
from .forms import CommentForm


def home(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    return render(request, 'main.html', {'articles': articles, 'categories': categories})

def biography_details(request, slug):
    article = get_object_or_404(Article, slug=slug)
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

    return render(request, 'biography_detail.html', {
        'articles': article,
        'tags': tags,
        'comments': comments,
        'form': form,
        'categories': categories
    })


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
