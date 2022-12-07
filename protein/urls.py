from django.conf.urls import url
from django.urls import path
from django.views.decorators.cache import cache_page
from ligand import views

urlpatterns = [
    #  url(r'^browser$', cache_page(3600*24*7)(views.LigandBrowser.as_view()), name='ligand_browser'),
    url(r'^proteinbrowser/$', cache_page(3600*24*7)
        (views.ProteinBrowser.as_view()), name='protein_browser'),

]
