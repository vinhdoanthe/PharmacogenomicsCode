from django.urls import path

from restapi.views import GeneDetailRestApiView

app_name = 'restapi'

urlpatterns = [
    path('gene/<slug:gene_id>/', GeneDetailRestApiView.as_view(), name='gene'),
]
