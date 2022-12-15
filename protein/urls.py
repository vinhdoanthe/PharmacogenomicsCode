# from django.conf.urls import url
from django.urls import path
from django.views.decorators.cache import cache_page
from .views import ProteinBrowser


urlpatterns = [
    #  url(r'^browser$', cache_page(3600*24*7)(views.LigandBrowser.as_view()), name='ligand_browser'),
    path('proteinbrowser',
         (ProteinBrowser.as_view()), name='protein_browser'),

]
