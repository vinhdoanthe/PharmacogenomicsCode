from django.urls import path, re_path
from .views import (
    GeneDetailBrowser,
    genebassVariantListView,
    filter_gene_detail_page
)

app_name = 'gene'

urlpatterns = [
    path('gene/<slug:slug>/', GeneDetailBrowser.as_view(), name='gene'),
    path('gene/<str:id>/filter', filter_gene_detail_page, name='filter-gene-detail-page'),
    path('gene/<str:pk>/genebass-variants/', genebassVariantListView.as_view(), name='genebass-variants'),
]
