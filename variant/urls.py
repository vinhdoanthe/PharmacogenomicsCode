from django.urls import path

from .views import get_genebass_tables

app_name = 'variant'

urlpatterns = [
    path('genebass-variants/', get_genebass_tables, name='get-genebass-tables'),
    ]
