from django.urls import path
from django.views.decorators.cache import cache_page
from .views import GeneBrowser


urlpatterns = [

    path('gene',
         (GeneBrowser.as_view()), name='gene'),

]
