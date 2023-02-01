from django.shortcuts import render
from gene.models import Gene
import json
from django.http import HttpResponse

# Create your views here.
def autocompleteModel(request):
    template_name = 'selection.html'
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Gene.objects.filter(name__startswith=q)
        results = []
        print (q)
        for r in search_qs:
            results.append(r.FIELD)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)