from django.urls import path
from django.views.decorators.cache import cache_page
from .views import DrugBrowser


urlpatterns = [

    path('drug',
         (DrugBrowser.as_view()), name='drug'),

]
