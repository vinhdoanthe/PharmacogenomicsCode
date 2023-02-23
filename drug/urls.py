from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import DrugBrowser, SelectionAutocomplete, detail, DrugStatistics
from  . import views


urlpatterns = [
    path('drugbrowser', views.drugbrowser, name='drugbrowser'),
    path('drug', (DrugBrowser.as_view()), name='drug'),
    path('drugstatistic', (DrugStatistics.as_view()), name='drug'),
    path('drug/autocomplete', (SelectionAutocomplete), name='autocomplete'),
    re_path(r'^drug/(?P<slug>[\w-]+)/$', views.detail, name='detail'),

]


