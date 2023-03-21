from django.urls import path, re_path
from  . import views
from .views import index

urlpatterns = [
    path('index', views.index, name='temp_index'),
]


