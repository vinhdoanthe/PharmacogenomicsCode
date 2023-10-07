# from django.conf.urls import url
from django.urls import path
from django.views.decorators.cache import cache_page
from .views import Home, drug_target_network


urlpatterns = [
    path("", Home.as_view(), name='home'),
    path("drug_target_network/", drug_target_network, name='drug_target_network'),
]
