from django.urls import path

from gene.views import GeneDetailApiView

app_name = 'api'

urlpatterns = (
    path('gene/<slug:gene_id>/', GeneDetailApiView.as_view(), name='gene'),
)
### API