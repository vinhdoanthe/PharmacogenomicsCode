from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import SelectionAutocomplete, DrugStatistics, drug_detail
from  . import views
from .views import search_drugs, drug_atc_expansion

urlpatterns = [
    path('search_drugs', views.search_drugs, name='search_drugs'),

    # This url should be update to include drugbank_id as a request parameters, see `'drug/<str:drugbank_id>/'`
    path('drug_atc', views.drug_atc_expansion, name='drug_atc'),
    
    path('drugbrowser', views.drugbrowser, name='drugbrowser'), #load all the drugs - cached but still slow - might need to remove
    path('drugstatistic', (DrugStatistics.as_view()), name='drug'), # okie but with dummy data
    path('drug/autocomplete', (SelectionAutocomplete), name='autocomplete'),
    path('drug/<str:drugbank_id>/', drug_detail, name='drug_detail'), # still ok but template does not have much info
]


