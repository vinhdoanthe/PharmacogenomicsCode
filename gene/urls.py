from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import GeneDetailBrowser, genebassVariantListView
from . import views

urlpatterns = [

    # path('gene', GeneBrowser.as_view(), name='gene'),
    # #  path('gene/autocomplete', (SelectionAutocomplete), name='autocomplete'),
    #  re_path(r'^gene/(?P<slug>[\w-]+)/$', views.detail, name='detail'),
    path('gene/<slug:slug>/', GeneDetailBrowser.as_view(), name='gene'),
    path('gene/<str:pk>/genebass-variants/', genebassVariantListView.as_view(), name='genebass-variants'),
]
