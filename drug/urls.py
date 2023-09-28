from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import SelectionAutocomplete, DrugStatistics
from . import views
from .views import search_drugs, drug_atc_expansion, atc_lookup, l2_atc_page_view, atc_search_view, get_drug_atc_association, get_drug_network

urlpatterns = [
    path('search_drugs', views.search_drugs, name='search_drugs'),
    path('atc_lookup', views.atc_lookup, name='atc_lookup'),
    path('atc_search_view', views.atc_search_view, name='atc_search_view'),
    path('l2_atc_page_view/', views.l2_atc_page_view, name='l2_atc_page_view'),
    path('get_drug_atc_association/', views.get_drug_atc_association, name='get-drug-atc-association'),
    path('get_drug_network/', views.get_drug_network, name='get-drug-network'),
    path('drugbrowser', views.drugbrowser, name='drugbrowser'),  # load all the drugs - cached but still slow - might need to remove
    path('drugstatistic', (DrugStatistics.as_view()), name='drug'),  # okie but with dummy data
    path('drug/autocomplete', (SelectionAutocomplete), name='autocomplete'),
    path('drug/<str:drugbank_id>/', views.drug_atc_expansion, name='drug_detail'),  # still ok but template does not have much info
]
