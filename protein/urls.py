# from django.conf.urls import url
from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import ProteinBrowser
from . import views


urlpatterns = [
    #  url(r'^browser$', cache_page(3600*24*7)(views.LigandBrowser.as_view()), name='ligand_browser'),
    path('protein',
         (ProteinBrowser.as_view()), name='protein_browser'),
    re_path(r'^protein/(?P<slug>[\w-]+)/$', views.detail, name='detail'), 
]
