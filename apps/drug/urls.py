from django.urls import path, re_path
from .views import SelectionAutocomplete, DrugStatistics
from . import views

urlpatterns = [
    path('search_drugs', views.search_drugs, name='search_drugs'),
    path('atc-lookup', views.atc_lookup, name='atc-lookup'),
    path('atc-anatomical-groups', views.AtcAnatomicalGroupListView.as_view(), name='atc-anatomical-groups'),
    path('atc_search_view', views.atc_search_view, name='atc_search_view'),
    path('atc-detail-view/', views.atc_detail_view, name='atc-detail-view'),
    path('get_drug_atc_association/', views.get_drug_atc_association, name='get-drug-atc-association'),
    path('get_drug_network/', views.get_drug_network, name='get-drug-network'),
    path('get-atc-sub-levels/', views.get_atc_sub_levels, name='get-atc-sub-levels'),
    path('drugbrowser', views.drugbrowser, name='drugbrowser'),  # load all the drugs - cached but still slow - might need to remove
    path('drugstatistic', (DrugStatistics.as_view()), name='drug'),  # okie but with dummy data
    path('drug/autocomplete', (SelectionAutocomplete), name='autocomplete'),
    path('drug/<str:drugbank_id>/', views.drug_atc_expansion, name='drug_detail'),  # still ok but template does not have much info
    path('get-drug-network-frame', views.get_drug_network_frame, name='get-drug-network-frame'),
    path('atc/<str:pk>/', views.AtcChemicalSubstanceDetailView.as_view(), name='atc_detail_view'),
]