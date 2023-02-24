from django.shortcuts import render

# Create your views here.
import hashlib
import itertools
import json
import os
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
from django.conf import settings
from drug.models import Drug
from gene.models import Gene
from interaction.models import Interaction
from protein.models import Protein
from variant.models import Variant
from django.core.cache import cache
from django.views.decorators.cache import cache_page


# Create your views here.
# class DrugAndTargetBrowser(TemplateView):

#     template_name = 'drug_browser copy.html'
#     # template_name = 'drugstatistics copy.html'

#     def get_context_data(self, **kwargs):

#         context = super().get_context_data(**kwargs)

#         browser_columns = ["gene_name",
#                            "interaction_type",
#                            "drugtype",
#                            "uniprot_ID",
#                            "geneID",
#                            "#variants"
#                            ]
#         table = pd.DataFrame(columns=browser_columns)

#         interaction_data = Interaction.objects.filter(drug_bankID='DB00002').values_list(
#             "uniprot_ID", "interaction_type")
#         drug_data = Drug.objects.filter(
#             drug_bankID='DB00002').values_list("drugtype", "name")
#         drug_data = Drug.objects.all().values_list("drugtype", "name")
#         drugname=drug_data[0][1]

#         if drug_data[0][0] == 1:
#             drugtype = "Biotech"
#         else:
#             drugtype = "Small molecule"
      
#         for data in interaction_data:
#             data_subset = {}
#             data_subset["uniprot_ID"] = data[0]
#             data_subset["interaction_type"] = data[1].title()
#             data_subset["drugtype"] = drugtype

#             # Retrieve protein name
#             genename = Protein.objects.filter(
#                 uniprot_ID=data[0]).values_list("genename")[0][0]
#             data_subset["gene_name"] = genename

#             # Retrieve gene ID
#             geneID = Protein.objects.filter(
#                 uniprot_ID=data[0]).values_list("geneID")[0][0]
#             data_subset["geneID"] = geneID

#             # Retrieve number of variant
#             markers = Variant.objects.filter(
#                 Gene_ID=geneID).values_list("VariantMarker")
#             data_subset["#variants"]=len(markers)

#             table = table.append(data_subset, ignore_index=True)
            

#         table.fillna('', inplace=True)
#         # context = dict()
#         print(table.head(3))
#         print("--------------------  drug_data[0][0]: ", drug_data[0][0])
#         length = len(table)
#         context['Array'] = table.to_numpy()
#         context['test'] = table.to_json(orient='records')
#         context['drugname'] = drugname
#         context['drugID'] = 'DB00002'
#         context['length'] = length

#         return context

#Create a dictionary for looking up encoded_term
drugdata_dic = {}
drugdata_data_dir = os.sep.join([settings.DATA_DIR, "drug_data"])
filepath = os.sep.join([drugdata_data_dir, "encoded_drug_data.txt"])
with open(filepath, "r") as f:
    lines = f.readlines()
    for line in lines:
        drugdata_dic[line[:-1].split(":")[0]] = line[:-1].split(":")[1]
# print(drugdata_dic)

def decode_drug_data(category, sub_cate):
    encoded_data_dict={'drugtype':"0", 
                       'name':"1",
                       'superclass':"2", 
                       'classname':"3", 
                       'subclass':"4", 
                       'direct_parent':"5",
                       'groups':"6", 
                       'categories':"7",
                       'pubChemCompound':"8",}
    encoded_term = encoded_data_dict.get(category)+"-"+str(sub_cate)
    
    return drugdata_dic.get(encoded_term)

    
@cache_page(60 * 60 * 24 * 28)
def drugbrowser(request):
    # Get drugdata from here somehow

    name_of_cache = 'drug_browser'

    context = cache.get(name_of_cache)

    if context == None:
        context = list()

        drugs = Drug.objects.all()

        for drug in drugs:
            drug_bankID = drug.drug_bankID
            drugtype = decode_drug_data("drugtype", drug.drugtype)
            drugname = decode_drug_data("name", drug.name)
            groups = decode_drug_data("groups", drug.groups)
            categories = decode_drug_data("categories", drug.categories)
            description = drug.description
            aliases = drug.aliases
            superclass = decode_drug_data("superclass", drug.superclass)
            classname = decode_drug_data("classname", drug.classname)
            subclass = decode_drug_data("subclass", drug.subclass)
            direct_parent = decode_drug_data("direct_parent", drug.direct_parent)
            indication = drug.indication
            pharmacodynamics = drug.pharmacodynamics
            moa = drug.moa
            absorption = drug.absorption
            toxicity = drug.toxicity
            halflife = drug.halflife
            distribution_volume = drug.distribution_volume
            protein_binding = drug.protein_binding
            dosages = drug.dosages
            properties = drug.properties
            atc_codes = drug.atc_codes
            atc_code_detail = drug.atc_code_detail
            chEMBL = drug.chEMBL
            pubChemCompound = decode_drug_data("pubChemCompound", drug.pubChemCompound)
            pubChemSubstance = drug.pubChemSubstance

            jsondata = {'drug_bankID':drug_bankID, 'drugtype':drugtype, 'drugname': drugname, 'groups':groups, 
                        'categories':categories, 'description':description, 'aliases':aliases, 'superclass':superclass, 
                        'classname':classname, 'subclass':subclass, 'direct_parent':direct_parent, 'indication':indication, 
                        'pharmacodynamics':pharmacodynamics, 'moa':moa, 'absorption':absorption, 'toxicity':toxicity, 
                        'halflife':halflife, 'distribution_volume':distribution_volume, 'protein_binding':protein_binding, 'dosages':dosages, 
                        'properties':properties, 'atc_codes':atc_codes, 'atc_code_detail':atc_code_detail, 'chEMBL':chEMBL, 
                        'pubChemCompound':pubChemCompound, 'pubChemSubstance':pubChemSubstance}
            context.append(jsondata)

        cache.set(name_of_cache, context, 60*60*24*28)

    return render(request, 'drug_browser copy.html', {'drugdata': context})
    
# Old way
class DrugBrowser(TemplateView):

    template_name = 'drug_browser copy.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        browser_columns = ["drug_bankID",
                            "drugtype",
                            "name",
                            "groups",
                            "categories",
                            "description",
                            "aliases",
                            "superclass",
                            "classname",
                            "subclass",
                            "direct_parent",
                            "indication",
                            "pharmacodynamics",
                            "moa",
                            "absorption",
                            "toxicity",
                            "halflife",
                            "distribution_volume",
                            "protein_binding",
                            "dosages",
                            "properties",
                            "atc_codes",
                            "atc_code_detail",
                            "chEMBL",
                            "pubChemCompound",
                            "pubChemSubstance"
                           ]
        table = pd.DataFrame(columns=browser_columns)
        drug_rows = Drug.objects.all().values_list("drug_bankID",
                                                    "drugtype",
                                                    "name",
                                                    "groups",
                                                    "categories",
                                                    "description",
                                                    "aliases",
                                                    "superclass",
                                                    "classname",
                                                    "subclass",
                                                    "direct_parent",
                                                    "indication",
                                                    "pharmacodynamics",
                                                    "moa",
                                                    "absorption",
                                                    "toxicity",
                                                    "halflife",
                                                    "distribution_volume",
                                                    "protein_binding",
                                                    "dosages",
                                                    "properties",
                                                    "atc_codes",
                                                    "atc_code_detail",
                                                    "chEMBL",
                                                    "pubChemCompound",
                                                    "pubChemSubstance")

        # if drug_data[0][0] == 1:
        #     drugtype = "Biotech"
        # else:
        #     drugtype = "Small molecule"
      
        for drug_data in drug_rows:
            data_subset = {}
            data_subset["drug_bankID"] = drug_data[0]
            data_subset["drugtype"] = drug_data[1]
            data_subset["name"] = drug_data[2]
            data_subset["groups"] = drug_data[3]
            data_subset["categories"] = drug_data[4]
            data_subset["description"] = drug_data[5]
            data_subset["aliases"] = drug_data[6]
            data_subset["superclass"] = drug_data[7]
            data_subset["classname"] = drug_data[8]
            data_subset["subclass"] = drug_data[9]
            data_subset["direct_parent"] = drug_data[10]
            data_subset["indication"] = drug_data[11]
            data_subset["pharmacodynamics"] = drug_data[12]
            data_subset["moa"] = drug_data[13]
            data_subset["absorption"] = drug_data[14]
            data_subset["toxicity"] = drug_data[15]
            data_subset["halflife"] = drug_data[16]
            data_subset["distribution_volume"] = drug_data[17]
            data_subset["protein_binding"] = drug_data[18]
            data_subset["dosages"] = drug_data[19]
            data_subset["properties"] = drug_data[20]
            data_subset["atc_codes"] = drug_data[21]
            data_subset["atc_code_detail"] = drug_data[22]
            data_subset["chEMBL"] = drug_data[23]
            data_subset["pubChemCompound"] = drug_data[24]
            data_subset["pubChemSubstance"] = drug_data[25]

            table = table.append(data_subset, ignore_index=True)
            

        table.fillna('', inplace=True)
        # context = dict()
        print(table.head(3))
        length = len(table)
        context['drugdata'] = table.to_numpy()
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
        # if type_of_selection!='navbar':
        #     ps = Protein.objects.filter(Q(name__icontains=q) | Q(entry_name__icontains=q),
        #                                 species__in=(species_list),
        #                                 source__in=(protein_source_list)).exclude(family__slug__startswith=exclusion_slug).exclude(sequence_type__slug='consensus')[:10]
        # else:
        #     print('checking that we are here')
        #     redirect = '/drug/'
        #     ps = Drug.objects.filter(Q(drug_bankID__icontains=q) | Q(name__icontains=q) | Q(aliases__icontains=q))
        #     if len(ps) == 0:
        #         redirect = '/gene/'
        #         ps = Gene.objects.filter(Q(gene_id__icontains=q) | Q(genename__icontains=q))
        # print("ps length ", ps.count())
        # print("ps ---------------", ps)

        if type_of_selection!='navbar':
            ps = Protein.objects.filter(Q(name__icontains=q) | Q(entry_name__icontains=q),
                                        species__in=(species_list),
                                        source__in=(protein_source_list)).exclude(family__slug__startswith=exclusion_slug).exclude(sequence_type__slug='consensus')[:10]
        else:
            print('checking that we are here')
            redirect = '/drug/'
            ps1 = Drug.objects.filter(Q(drug_bankID__icontains=q) | Q(name__icontains=q) | Q(aliases__icontains=q))
            ps2 = Gene.objects.filter(Q(gene_id__icontains=q) | Q(genename__icontains=q))
            ps3 = Protein.objects.filter(Q(uniprot_ID__icontains=q) | Q(protein_name__icontains=q))
            if len(ps1) > 0:
                redirect = '/drug/'
                ps = ps1
            if len(ps2) > 0:
                redirect = "/gene/"
                ps = ps2
            if len(ps3) > 0:
                redirect = "/protein/"
                ps = ps3
                
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
        else:
            if redirect == '/gene/':
                for p in ps:
                    p_json = {}
                    p_json['id'] = p.gene_id
                    p_json['type'] = 'Gene'
                    p_json['category'] = 'Genes'
                    p_json['label'] = p.genename
                    p_json['redirect'] = redirect
                    results.append(p_json)
            else:
                if redirect == "/protein/":
                    for p in ps:
                        p_json = {}
                        p_json['id'] = p.uniprot_ID
                        p_json['type'] = 'Protein'
                        p_json['category'] = 'Proteins'
                        p_json['label'] = p.protein_name
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


# Create your views here.
class DrugStatistics(TemplateView):

    template_name = 'drugstatistics copy.html'

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