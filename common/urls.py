from django.conf.urls import url
from django.urls import path
from .views import autocompleteModel


urlpatterns = [
    url(r'^ajax_calls/search/', autocompleteModel),
]

