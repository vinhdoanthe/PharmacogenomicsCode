from django.shortcuts import render, get_object_or_404

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
from drug.models import Drug, DrugAtcAssociation, AtcAnatomicalGroup, AtcTherapeuticGroup, AtcPharmacologicalGroup, AtcChemicalGroup, AtcChemicalSubstance
from gene.models import Gene
from interaction.models import Interaction
from django.db.models import Count
from protein.models import Protein
from variant.models import Variant
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.template.loader import render_to_string

# Create your views here.
from django.http import JsonResponse
from .models import Drug, DrugAtcAssociation

app_name = 'drug'

# Then in this view function, we add drugbank_id as a parameter
def drug_atc_expansion(request, drugbank_id): #put a parameter drugbank_id here

    context={}

    # Specify the drug of interest
    drug_name = "Insulin human"

    # Retrieve the drug object based on the name
    # And change the code getting drug to bellow
    # drug = get_object_or_404(Drug, drug_bankID=drugbank_id)
    drug = Drug.objects.get(drug_bankID=drugbank_id)
    # print("Drug: ", drug)

    # Get the related ATC code of the drug
    atc_code = DrugAtcAssociation.objects.filter(drug_id=drug).values_list('atc_id_id')
    context["num_substance"] = len(atc_code)
    num_list = [num + 1 for num in range(len(atc_code))]
    context ['num_list'] = num_list
    atc_anatomical_group_list = list(set([x[0][0]+" ("+AtcAnatomicalGroup.objects.filter(id=x[0][0]).values_list('name', flat=True)[0]+")" for x in atc_code]))
    atc_therapeutic_group_list = list(set([x[0][:3]+" ("+AtcTherapeuticGroup.objects.filter(id=x[0][0:3]).values_list('name', flat=True)[0]+")" for x in atc_code]))
    atc_pharmacological_group_list = list(set([x[0][:4]+" ("+AtcPharmacologicalGroup.objects.filter(id=x[0][0:4]).values_list('name', flat=True)[0]+")" for x in atc_code]))
    atc_chemical_group_list = list(set([x[0][:5]+" ("+AtcChemicalGroup.objects.filter(id=x[0][0:5]).values_list('name', flat=True)[0]+")" for x in atc_code]))
    atc_chemical_substance_list = list(set([x[0]+" ("+AtcChemicalSubstance.objects.filter(id=x[0][0:7]).values_list('name', flat=True)[0]+")" for x in atc_code]))
    print("atc_anatomical_group_list : ", atc_anatomical_group_list)
    print("atc_therapeutic_group_list : ", atc_therapeutic_group_list)
    print("atc_pharmacological_group_list : ", atc_pharmacological_group_list)
    print("atc_chemical_group_list : ", atc_chemical_group_list)
    print("atc_chemical_substance_list : ", atc_chemical_substance_list)


    drugListDict = {}
    # codeNameListDict = {}
    for code in atc_anatomical_group_list:
        temp = DrugAtcAssociation.objects.filter(atc_id__id__startswith=code).values_list('drug_id__drug_bankID', flat=True)
        drugListDict[code] = list(set([item for item in temp]))
        # name=AtcAnatomicalGroup.objects.filter(id=code).values_list('name', flat=True)[0]
        # codeNameListDict[code]=name
    for code in atc_therapeutic_group_list:
        temp = DrugAtcAssociation.objects.filter(atc_id__id__startswith=code).values_list('drug_id__drug_bankID', flat=True)
        drugListDict[code] = list(set([item for item in temp]))
        # name=AtcTherapeuticGroup.objects.filter(id=code).values_list('name', flat=True)[0]
        # codeNameListDict[code]=name
    for code in atc_pharmacological_group_list:
        temp = DrugAtcAssociation.objects.filter(atc_id__id__startswith=code).values_list('drug_id__drug_bankID', flat=True)
        drugListDict[code] = list(set([item for item in temp]))
        # name=AtcPharmacologicalGroup.objects.filter(id=code).values_list('name', flat=True)[0]
        # codeNameListDict[code]=name
    for code in atc_chemical_group_list:
        temp = DrugAtcAssociation.objects.filter(atc_id__id__startswith=code).values_list('drug_id__drug_bankID', flat=True)
        drugListDict[code] = list(set([item for item in temp]))
        # name=AtcChemicalGroup.objects.filter(id=code).values_list('name', flat=True)[0]
        # codeNameListDict[code]=name
    for code in atc_chemical_substance_list:
        temp = DrugAtcAssociation.objects.filter(atc_id__id__startswith=code).values_list('drug_id__drug_bankID', flat=True)
        drugListDict[code] = list(set([item for item in temp]))
        # name=AtcChemicalSubstance.objects.filter(id=code).values_list('name', flat=True)[0]
        # codeNameListDict[code]=name

    # print("codeNameListDict : ", codeNameListDict)
        



    # Convert the list to a JSON string
    json_drugList_data = json.dumps(drugListDict)
    # json_codeName_data = json.dumps(codeNameListDict)
    # print("json_data: ", json_data)

    # Pass the JSON string to the template context
    context['json_drugList_data'] = json_drugList_data
    context['drugListDict'] = drugListDict
    # context['codeNameListDict'] = codeNameListDict
    # context['json_codeName_data'] = json_codeName_data
    context['atc_anatomical_group_list'] = atc_anatomical_group_list
    context['atc_therapeutic_group_list'] = atc_therapeutic_group_list
    context['atc_pharmacological_group_list'] = atc_pharmacological_group_list
    context['atc_chemical_group_list'] = atc_chemical_group_list
    context['atc_chemical_substance_list'] = atc_chemical_substance_list

    # return render(request, 'drug_atc_tabs.html', context)
    return render(request, 'drug_atc_tabs_horizontal.html', context)
    # return render(request, 'drug_atc_tabs-leftshape.html', context)


def search_drugs(request):
    #extracts the search query parameter named 'q' from the GET request's query parameters. If 'q' is not present, the variable query is assigned the value None
    query = request.GET.get('q')

    # This line filters the Drug model's objects based on the search query. It uses the icontains lookup to perform a case-insensitive search on both the name and aliases fields, using the '|' (OR) operator to combine the two queries.
    drugs = Drug.objects.filter(Q(name__icontains=query) | Q(aliases__icontains=query))

    # creates a list of distinct drug names from the queryset drugs. The values_list method retrieves a list of tuples containing the 'name' field values, and the flat=True argument turns it into a flat list. The distinct() method ensures that only unique drug names are included.
    drug_names = drugs.values_list('name', flat=True).distinct()

    # Get related ATC codes and associated drugs for each drug
    drug_info = []
    for drug in drugs:
        #filters the DrugAtcAssociation model's objects based on the drug's ATC associations. It selects objects whose 'atc_id' is included in the drug's related ATC associations.
        drug_atc_associations = DrugAtcAssociation.objects.filter(atc_id__in=drug.drugatcassociation.all())
        atc_codes = drug_atc_associations.values_list('atc_id__id', flat=True).distinct()

        atc_drug_map = {}
        for atc_code in atc_codes:
            associated_drugs = Drug.objects.filter(drugatcassociation__atc_id__id=atc_code)
            atc_drug_map[atc_code] = associated_drugs

        drug_info.append({
            'name': drug.name,
            'related_atc_codes': atc_codes,
            'atc_drug_map': atc_drug_map,
        })

    # Pass the list of drug names and related drug information to the template for rendering
    context = {
        'drug_names': drug_names,
        'query': query,
        'drug_info': drug_info,
    }
    return render(request, 'drug_search_results.html', context)



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

            #retrieve drugtype
            drug = Drug.objects.select_related('drugtype').filter(drug_bankID=drug_bankID).first()
            if drug:
                drugtype = drug.drugtype.type_detail
            else:
                drugtype = None

            #retrieve drugname
            drugname = drug.name

            #retrieve groups
            drug = Drug.objects.select_related('groups').filter(drug_bankID=drug_bankID).first()
            if drug:
                groups = drug.groups.group_detail
            else:
                groups = None

            #retrieve categories
            drug = Drug.objects.select_related('categories').filter(drug_bankID=drug_bankID).first()
            if drug:
                categories = drug.categories.category_detail
            else:
                categories = None

            #retrieve description
            description = drug.description

            #retrieve superclass
            drug = Drug.objects.select_related('superclass').filter(drug_bankID=drug_bankID).first()
            if drug:
                superclass = drug.superclass.superclass_detail
            else:
                superclass = None

            #retrieve classname
            drug = Drug.objects.select_related('classname').filter(drug_bankID=drug_bankID).first()
            if drug:
                classname = drug.classname.class_detail
            else:
                classname = None

            #retrieve subclass
            drug = Drug.objects.select_related('subclass').filter(drug_bankID=drug_bankID).first()
            if drug:
                subclass = drug.subclass.subclass_detail
            else:
                subclass = None

            #retrieve direct_parent
            drug = Drug.objects.select_related('direct_parent').filter(drug_bankID=drug_bankID).first()
            if drug:
                direct_parent = drug.direct_parent.parent_detail
            else:
                direct_parent = None

            description = drug.description
            aliases = drug.aliases
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
            chEMBL = drug.chEMBL

            # retrieve pubChemCompound
            drug = Drug.objects.select_related('pubChemCompound').filter(drug_bankID=drug_bankID).first()
            if drug:
                pubChemCompound = drug.pubChemCompound.compound_detail
            else:
                pubChemCompound = None

            pubChemSubstance = drug.pubChemSubstance

            jsondata = {'drug_bankID':drug_bankID, 'drugtype':drugtype, 'drugname': drugname, 'groups':groups,
                        'categories':categories, 'description':description, 'aliases':aliases, 'superclass':superclass,
                        'classname':classname, 'subclass':subclass, 'direct_parent':direct_parent, 'indication':indication,
                        'pharmacodynamics':pharmacodynamics, 'moa':moa, 'absorption':absorption, 'toxicity':toxicity,
                        'halflife':halflife, 'distribution_volume':distribution_volume, 'protein_binding':protein_binding, 'dosages':dosages,
                        'properties':properties, 'chEMBL':chEMBL,
                        'pubChemCompound':pubChemCompound, 'pubChemSubstance':pubChemSubstance}
            context.append(jsondata)

        cache.set(name_of_cache, context, 60*60*24*28)

    return render(request, 'drug_browser copy.html', {'drugdata': context})



# This is a helper function that takes a request object and checks if it's an AJAX request. It does this by checking if the 'HTTP_X_REQUESTED_WITH' key in the request.META dictionary is set to 'XMLHttpRequest'. If it is, it returns True, otherwise it returns False.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def SelectionAutocomplete(request):

    if is_ajax(request=request):

        #This line gets the 'term' parameter from the GET data of the request, removes any leading and trailing whitespace, and assigns the result to the variable 'q'. The 'term' parameter is the search term entered by the user.
        q = request.GET.get('term').strip()
        type_of_selection = request.GET.get('type_of_selection')
        results = []


        if type_of_selection!='navbar':
            ps = Protein.objects.filter(Q(name__icontains=q) | Q(entry_name__icontains=q),
                                        species__in=(species_list),
                                        source__in=(protein_source_list)).exclude(family__slug__startswith=exclusion_slug).exclude(sequence_type__slug='consensus')[:10]
        else:
            ps = []
            print('Checking that we are here')
            redirect = '/drug/'
            ps1 = Drug.objects.filter(Q(drug_bankID__icontains=q) | Q(name__icontains=q) | Q(aliases__icontains=q))
            ps2 = Gene.objects.filter(Q(gene_id__icontains=q) | Q(genename__icontains=q))
            ps3 = Protein.objects.filter(Q(uniprot_ID__icontains=q) | Q(protein_name__icontains=q))
            # ps4 = Protein.objects.filter(Q(uniprot_ID__icontains=q) | Q(protein_name__icontains=q))
            # if len(ps1) > 0:
            #     redirect = '/drug/'
            #     ps = ps1
            # if len(ps2) > 0:
            #     redirect = "/gene/"
            #     ps = ps2
            # if len(ps3) > 0:
            #     redirect = "/protein/"
            #     ps = ps3

        for p in ps1:
            p_json = {}
            p_json['id'] = p.drug_bankID
            p_json['label'] = p.name
            p_json['type'] = 'drug'
            p_json['redirect'] = '/drug/'
            p_json['category'] = 'Drugs'
            results.append(p_json)

        for p in ps2:
            p_json = {}
            p_json['id'] = p.gene_id
            p_json['type'] = 'Gene'
            p_json['category'] = 'Genes'
            p_json['label'] = p.genename
            p_json['redirect'] = '/gene/'
            results.append(p_json)  
        
        for p in ps3:
            p_json = {}
            p_json['id'] = p.uniprot_ID
            p_json['type'] = 'Protein'
            p_json['category'] = 'Proteins'
            p_json['label'] = p.protein_name
            p_json['redirect'] = '/protein/'
            results.append(p_json)
            

        # if redirect == '/drug/':
        #     for p in ps:
        #         p_json = {}
        #         p_json['id'] = p.drug_bankID
        #         p_json['label'] = p.name
        #         p_json['type'] = 'drug'
        #         p_json['redirect'] = redirect
        #         p_json['category'] = 'Drugs'
        #         results.append(p_json)
        # else:
        #     if redirect == '/gene/':
        #         for p in ps:
        #             p_json = {}
        #             p_json['id'] = p.gene_id
        #             p_json['type'] = 'Gene'
        #             p_json['category'] = 'Genes'
        #             p_json['label'] = p.genename
        #             p_json['redirect'] = redirect
        #             results.append(p_json)
        #     else:
        #         if redirect == "/protein/":
        #             for p in ps:
        #                 p_json = {}
        #                 p_json['id'] = p.uniprot_ID
        #                 p_json['type'] = 'Protein'
        #                 p_json['category'] = 'Proteins'
        #                 p_json['label'] = p.protein_name
        #                 p_json['redirect'] = redirect
        #                 results.append(p_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    #return an HTTP response containing the data in JSON format, which is specified by the 'application/json' mimetype
    #JSON format can be understood by the browser and other clients as a JavaScript object. This could be useful if the view is returning data that is meant to be consumed by JavaScript code running on the client side
    return HttpResponse(data, mimetype)


# Create your views here.
class DrugStatistics(TemplateView):

    template_name = 'drugstatistics.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Help from chatGPT.
def drug_interaction_detail(request, drugbank_id):
    # Retrieve the drug object
    drug = get_object_or_404(Drug, drug_bankID=drugbank_id)

    # a) Retrieve all the uniprot_ID of proteins that have interactions with the drug
    interactions = Interaction.objects.filter(drug_bankID=drug)
    protein_ids = [interaction.uniprot_ID.uniprot_ID for interaction in interactions]

    # b) Count for each interaction_type
    interaction_counts = interactions.values('interaction_type').annotate(count=Count('interaction_type'))

    # c) Retrieve the names of all AtcChemicalSubstance that associate with the drugs
    associations = DrugAtcAssociation.objects.filter(drug_id=drug)
    chemical_substance_names = [association.atc_id.id + "-"+ association.atc_id.name for association in associations]

    # d) For each AtcChemicalSubstance, retrieve their parents until the top one
    atc_parents = []
    for association in associations:
        temp=[]
        parent = association.atc_id.parent
        temp.append(parent.id + "-" + parent.name)
        while parent:
            if not(isinstance(parent, AtcAnatomicalGroup)):
                parent = parent.parent
                temp.append(parent.id + "-" + parent.name)
            else:
                break
        atc_parents.append(temp)

    context = {
        'drug': drug,
        'protein_ids': protein_ids,
        'interaction_counts': interaction_counts,
        # 'associations': associations,
        'chemical_substance_names': chemical_substance_names,
        'atc_parents': atc_parents
    }

    print("-------------- context", context)
    # return render(request, '_drug_detail.html', context)
    return render(request, 'drug_atc_tabs.html', context)



def atc_lookup(request):

    group1s = AtcAnatomicalGroup.objects.all()
    # Uppercase the names before returning
    for group in group1s:
        group.name = group.name.upper()

    group2s = AtcTherapeuticGroup.objects.all()
    # Uppercase the names before returning
    for group in group2s:
        group.name = group.name.upper()

    context = {'group1s': group1s, 'group2s': group2s}
    return render(request, 'atc_code_lookup.html', context)

def format_atc_name(s):
    s=s.replace('"','')
    return s.upper()      


def l2_atc_page_view(request):
    group_id = request.GET.get('group_id')  # Retrieve group_id from the query parameter
    group_name = request.GET.get('group_name')
    group2s = AtcTherapeuticGroup.objects.all()
    for group in group2s:
        group.name = format_atc_name(group.name)
    group3s = AtcPharmacologicalGroup.objects.all()
    for group in group3s:
        group.name = format_atc_name(group.name)
    group4s = AtcChemicalGroup.objects.all()
    for group in group4s:
        group.name = format_atc_name(group.name)
    group5s = AtcChemicalSubstance.objects.all()
    for group in group5s:
        group.name = format_atc_name(group.name)
    context = {'group2s': group2s, 'group3s': group3s, 'group4s': group4s, 'group5s': group5s, "group_id": group_id, "group_name": group_name}
    return render(request, 'l2_atc_page_view.html', context)



@csrf_exempt  # Use this decorator for simplicity, but consider using a proper csrf token in production.
def atc_search_view(request):
    results = []
    print("*****************: ", request.method)
    if request.method == 'GET':
        atc_code_inp = request.GET.get('atc_code_inp', '').strip()
        atc_name_inp = request.GET.get('atc_name_inp', '').strip()
        query_option = request.GET.get('query_option', '')

        if atc_code_inp!="":
            # Search "id" field in all models
            print("branch in atc code, atc_code_inp = ", atc_code_inp)
            if len(atc_code_inp)>7:
                print("invalid atc_code_inp")
            else:
                if len(atc_code_inp)>5: #search for id length =7
                    results += list(AtcChemicalSubstance.objects.filter(id__iexact=atc_code_inp).values('id', 'name'))
                else:
                    if len(atc_code_inp)==5: #search for id length =5
                        results += list(AtcChemicalGroup.objects.filter(id__iexact=atc_code_inp).values('id', 'name'))
                    else:
                        if len(atc_code_inp)==4: #search for id length =5
                            results += list(AtcPharmacologicalGroup.objects.filter(id__iexact=atc_code_inp).values('id', 'name'))
                        else:
                            if len(atc_code_inp)==3: #search for id length =5
                                results += list(AtcTherapeuticGroup.objects.filter(id__iexact=atc_code_inp).values('id', 'name'))
                            else:
                                results += list(AtcAnatomicalGroup.objects.filter(id__iexact=atc_code_inp).values('id', 'name'))
        if atc_name_inp!="":
            if query_option == 'containing':
                # Search "name" field in all models
                print("branch in containing, atc_name_inp = ", atc_name_inp)
                results += list(AtcAnatomicalGroup.objects.filter(name__icontains=atc_name_inp).values('id', 'name'))
                results += list(AtcTherapeuticGroup.objects.filter(name__icontains=atc_name_inp).values('id', 'name'))
                results += list(AtcPharmacologicalGroup.objects.filter(name__icontains=atc_name_inp).values('id', 'name'))
                results += list(AtcChemicalGroup.objects.filter(name__icontains=atc_name_inp).values('id', 'name'))
                results += list(AtcChemicalSubstance.objects.filter(name__icontains=atc_name_inp).values('id', 'name'))

            elif query_option == 'startingwith':
                # Search "id" field in all models
                print("branch in startingwith, atc_name_inp = ", atc_name_inp)
                results += list(AtcAnatomicalGroup.objects.filter(name__startswith=atc_name_inp).values('id', 'name'))
                results += list(AtcTherapeuticGroup.objects.filter(name__startswith=atc_name_inp).values('id', 'name'))
                results += list(AtcPharmacologicalGroup.objects.filter(name__startswith=atc_name_inp).values('id', 'name'))
                results += list(AtcChemicalGroup.objects.filter(name__startswith=atc_name_inp).values('id', 'name'))
                results += list(AtcChemicalSubstance.objects.filter(name__startswith=atc_name_inp).values('id', 'name'))
        
        for rs in results:
            rs["name"] = format_atc_name(rs["name"])
        context = {"query_option":query_option, "search_result": results, "atc_code_inp": atc_code_inp, "atc_name_inp":atc_name_inp}
        return render(request, 'atc_search_result.html', context)
    return render(request, 'atc_search_result.html', {"results":results})



def get_drug_atc_association(request):
    atc_code = request.GET.get("atc_code")

    # Query the DrugAtcAssociation model and select related Drug fields
    associations = DrugAtcAssociation.objects.filter(atc_id=atc_code).select_related('drug_id')

    # Convert queryset to a list of dictionaries
    associations_list = [{"drug_bankID": assoc.drug_id.drug_bankID, "name": assoc.drug_id.name, "description": assoc.drug_id.description} for assoc in associations]

    # Create a JSON response with the data
    response_data = {
        "associations": associations_list,
        "atc_code":atc_code,
    }
    return JsonResponse(response_data)


def get_drug_network(request):
    drugbank_id = request.GET.get('drugbank_id')

    try:
        # Query the Drug model to get the drug object with the specified drug_bankID
        drug = Drug.objects.get(drug_bankID=drugbank_id)

        # Use select_related to retrieve related Interaction and Protein objects efficiently
        interactions = Interaction.objects.filter(drug_bankID=drug)

        # Create a list to store information
        response_data = []

        # Loop through the interactions to access related Protein objects
        for interaction in interactions:
            info = {}
            protein_id = interaction.uniprot_ID_id
            protein_obj = Protein.objects.get(uniprot_ID=protein_id)
            info["uniProt_id"] = protein_obj.uniprot_ID
            info["gene_name"] = protein_obj.genename
            info["gene_id"] = protein_obj.geneID
            info["protein_name"] = protein_obj.protein_name
            info["protein_class"] = protein_obj.Protein_class
            info["interaction_type"] = interaction.interaction_type
            info["pubmed_ids"] = interaction.pubmed_ids

            # Create a dictionary with the drug and related information
            response_data.append(info)

        # Wrap the response_data list in a dictionary with a key
        data = {'drug_network_data': response_data}
        print("data", data)

        # Return JsonResponse with safe=False
        return JsonResponse(data, safe=False)

    except Drug.DoesNotExist:
        return JsonResponse({"error": f"No drug with drug_bankID '{drugbank_id}' found."}, status=404)


def retrieving_anatomical_group (atc_code):
    return list(AtcAnatomicalGroup.objects.filter(id__iexact=atc_code).values('id', 'name'))
def retrieving_therapeutic_group (atc_code):
    return list(AtcTherapeuticGroup.objects.filter(id__startswith=atc_code).values('id', 'name'))
def retrieving_pharmacological_group (atc_code):
    return list(AtcPharmacologicalGroup.objects.filter(id__startswith=atc_code).values('id', 'name'))
def retrieving_chemical_group (atc_code):
    return list(AtcChemicalGroup.objects.filter(id__startswith=atc_code).values('id', 'name'))
def retrieving_chemical_substance (atc_code):
    return list(AtcChemicalSubstance.objects.filter(id__startswith=atc_code).values('id', 'name'))

def get_atc_sub_levels(request):
    atc_code = request.GET.get("atc_code");
    data = {'atc_code': atc_code}
    if len(atc_code)==1:
        data = {"anatomical_group": retrieving_anatomical_group (atc_code), "therapeutic_group": retrieving_therapeutic_group (atc_code),
                "pharmacological_group": retrieving_pharmacological_group (atc_code), "chemical_group": retrieving_chemical_group (atc_code), 
                "chemical_substance": retrieving_chemical_substance (atc_code)}
    if len(atc_code)==3:
        data = {"therapeutic_group": retrieving_therapeutic_group (atc_code),
                "pharmacological_group": retrieving_pharmacological_group (atc_code), "chemical_group": retrieving_chemical_group (atc_code), 
                "chemical_substance": retrieving_chemical_substance (atc_code)}
    if len(atc_code)==4:
        data = {"pharmacological_group": retrieving_pharmacological_group (atc_code), "chemical_group": retrieving_chemical_group (atc_code), 
                "chemical_substance": retrieving_chemical_substance (atc_code)}
    if len(atc_code)==5:
        data = {"chemical_group": retrieving_chemical_group (atc_code), 
                "chemical_substance": retrieving_chemical_substance (atc_code)}
    if len(atc_code)==7:
        data = {"chemical_substance": retrieving_chemical_substance (atc_code)}

    #re-organize the data
    reorganized_data = {}

    # Loop through each element in the original data
    for group_type, group_list in data.items():
        # Create a dictionary to hold the grouped elements
        grouped_elements = {}
        
        # Loop through the elements in the group_list
        for element in group_list:
            # Extract the element ID
            element_id = element['id']
            
            # Add the element to the grouped_elements dictionary
            grouped_elements[element_id] = element
        
        # Add the grouped_elements to the reorganized_data using the group_type as the key
        reorganized_data[group_type] = grouped_elements
    reorganized_data["atc_code"] = atc_code
    # print("data : ", reorganized_data)
    return JsonResponse(reorganized_data, safe=False)