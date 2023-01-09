from django.urls import path
from django.views.decorators.cache import cache_page
from .views import DrugPaginationBrowser


urlpatterns = [

    path('drug_pagination',
         (DrugPaginationBrowser.as_view()), name='drug_pagination'),

]
