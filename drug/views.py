import hashlib
import itertools
import json
import re
import time
import pandas as pd
import urllib
from random import SystemRandom
from copy import deepcopy
from collections import defaultdict, OrderedDict
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView
from django.db.models import Q, Count, Subquery, OuterRef
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from drug.models import Drug
from gene.models import Gene
from interaction.models import Interaction
from protein.models import Protein
from variantmarker.models import VariantMarker
from django.core.cache import cache
from django.views.decorators.cache import cache_page


# Create your views here.
class DrugBrowser(TemplateView):

    template_name = 'drug_browser copy.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        browser_columns = ["gene_name",
                           "interaction_type",
                           "drugtype",
                           "uniprot_ID",
                           "geneID",
                           "#variants"
                           ]
        table = pd.DataFrame(columns=browser_columns)

        interaction_data = Interaction.objects.filter(drug_bankID='DB00002').values_list(
            "uniprot_ID", "interaction_type")
        drug_data = Drug.objects.filter(
            drug_bankID='DB00002').values_list("drugtype", "name")
        drug_data = Drug.objects.all().values_list("drugtype", "name")
        drugname=drug_data[0][1]

        if drug_data[0][0] == 1:
            drugtype = "Biotech"
        else:
            drugtype = "Small molecule"
      
        for data in interaction_data:
            data_subset = {}
            data_subset["uniprot_ID"] = data[0]
            data_subset["interaction_type"] = data[1].title()
            data_subset["drugtype"] = drugtype

            # Retrieve protein name
            genename = Protein.objects.filter(
                uniprot_ID=data[0]).values_list("genename")[0][0]
            data_subset["gene_name"] = genename

            # Retrieve gene ID
            geneID = Protein.objects.filter(
                uniprot_ID=data[0]).values_list("geneID")[0][0]
            data_subset["geneID"] = geneID

            # Retrieve number of variant
            markers = VariantMarker.objects.filter(
                geneID=geneID).values_list("markerID")
            data_subset["#variants"]=len(markers)

            table = table.append(data_subset, ignore_index=True)
            

        table.fillna('', inplace=True)
        # context = dict()
        print(table.head(3))
        print("--------------------  drug_data[0][0]: ", drug_data[0][0])
        length = len(table)
        context['Array'] = table.to_numpy()
        context['test'] = table.to_json(orient='records')
        context['drugname'] = drugname
        context['drugID'] = 'DB00002'
        context['length'] = length

        return context

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def SelectionAutocomplete(request):

    if is_ajax(request=request):

        #This line gets the 'term' parameter from the GET data of the request, removes any leading and trailing whitespace, and assigns the result to the variable 'q'. The 'term' parameter is the search term entered by the user.
        q = request.GET.get('term').strip()
        type_of_selection = request.GET.get('type_of_selection')
        results = []

        # find proteins
        if type_of_selection!='navbar':
            ps = Protein.objects.filter(Q(name__icontains=q) | Q(entry_name__icontains=q),
                                        species__in=(species_list),
                                        source__in=(protein_source_list)).exclude(family__slug__startswith=exclusion_slug).exclude(sequence_type__slug='consensus')[:10]
        else:
            print('checking that we are here')
            redirect = '/drug/'
            ps = Drug.objects.filter(Q(drug_bankID__icontains=q) | Q(name__icontains=q) | Q(aliases__icontains=q))
            if len(ps) == 0:
                redirect = '/gene/'
                ps = Gene.objects.filter(Q(gene_id__icontains=q) | Q(genename__icontains=q))
        print("ps length ", ps.count())
        print("ps ---------------", ps)
        
        if redirect == '/drug/':
            for p in ps:
                p_json = {}
                p_json['id'] = p.drug_bankID
                p_json['label'] = p.name
                p_json['type'] = 'drug'
                p_json['redirect'] = redirect
                p_json['category'] = 'Drugs'
                results.append(p_json)
        elif redirect == '/gene/':
            for p in ps:
                p_json = {}
                p_json['id'] = p.gene_id
                p_json['type'] = 'Gene'
                p_json['category'] = 'Genes'
                p_json['label'] = p.genename
                p_json['redirect'] = redirect
                results.append(p_json)



        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    #return an HTTP response containing the data in JSON format, which is specified by the 'application/json' mimetype
    #JSON format can be understood by the browser and other clients as a JavaScript object. This could be useful if the view is returning data that is meant to be consumed by JavaScript code running on the client side
    return HttpResponse(data, mimetype)



#@cache_page(60 * 60 * 24 * 7)
def detail(request, slug):
    # get protein
    slug = slug.upper()

    print("SLUGGGGGGGGGGGGG", slug)
    print("SLUGGGGGGGGGGGGG", slug)
    print("SLUGGGGGGGGGGGGG", slug)
    print("SLUGGGGGGGGGGGGG", slug)
    try:
        if Drug.objects.filter(drug_bankID=slug).exists():
            p = Drug.objects.get(drug_bankID=slug)
            print("p --------- ",p)
        
    except:
        context = {'drug_no_found': slug}
        return render(request, 'drug_detail.html', context)

    # context_list=[]
    # for p in ps:

    # get family list
    id = p.drug_bankID
    drugtype = "Biotech" if p.drugtype == 1 else "Small molecule"
    name = p.name
    groups = p.groups
    categories = p.categories
    description = p.description
    aliases = p.aliases
    kingdom = p.kingdom
    superclass = p.superclass
    classname = p.classname
    subclass = p.subclass
    direct_parent = p.direct_parent
    indication = p.indication
    pharmacodynamics = p.pharmacodynamics
    moa = p.moa
    absorption = p.absorption
    toxicity = p.toxicity
    halflife = p.halflife
    distribution_volume = p.distribution_volume
    protein_binding = p.protein_binding
    dosages = p.dosages
    properties = p.properties


    context = {'drug_bankID': id, 'drugtype': drugtype, 'name': name, 'groups': groups, 'categories': categories,
            'description': description, 'aliases': aliases, 'kingdom': kingdom, 'superclass': superclass, 'classname': classname,'subclass': subclass, 'direct_parent':direct_parent, 'indication':indication, 'pharmacodynamics':pharmacodynamics, 'moa':moa, 'absorption':absorption, 'toxicity':toxicity, 'halflife':halflife, 'distribution_volume':distribution_volume, 'protein_binding':protein_binding, 'dosages':dosages, 'properties':properties}

        # context_list.append(dic)


    return render(request, 'drug_detail.html', context)