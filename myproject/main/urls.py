from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('biography/<slug:slug>/', views.biography_details, name='biography_details'),

    path('biography/', views.biography, name='biography'),

    path('category/<slug:slug>/', views.category_details, name='category_details'),

    path('category/', views.category, name='category'),

    path('search/', views.search_articles, name='search_articles'),
]
