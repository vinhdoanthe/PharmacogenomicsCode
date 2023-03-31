from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from  . import views
from .views import drug_atc_expansion

urlpatterns = [
    path('draft_drug_atc', views.drug_atc_expansion, name='draft_drug_atc'),
]


