# from django.conf.urls import url
from django.urls import path
from django.views.decorators.cache import cache_page
from .views import Home


urlpatterns = [
    path('home',
         (Home.as_view()), name='home'),
    
]
