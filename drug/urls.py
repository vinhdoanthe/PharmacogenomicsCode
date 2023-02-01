from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import DrugBrowser, SelectionAutocomplete, detail
from  . import views


urlpatterns = [

    path('drug', (DrugBrowser.as_view()), name='drug'),
    path('drug/autocomplete', (SelectionAutocomplete), name='autocomplete'),
    re_path(r'^drug/(?P<slug>[\w-]+)/$', views.detail, name='detail'),

]


