from django.urls import path
from django.views.decorators.cache import cache_page
from .views import home, about, PostListView, PostDetailView
from . import views


urlpatterns = [

    # path('home',
    #      (views.home), name='home'),
    path('about',
         (views.about), name='about'),
    path('home',
         (PostListView.as_view()), name='home'),

    path('post/<int:pk>',
         (PostDetailView.as_view()), name='blog_detail'),


]
