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


# Create your views here.
from django.http import JsonResponse

def drug_atc_expansion(request): #put a parameter drug_name here

    context={}

    # Specify the drug of interest
    drug_name = "Insulin human"

    # Retrieve the drug object based on the name
    drug = Drug.objects.get(name=drug_name)
    print("Drug: ", drug)

    # Get the related ATC code of the drug
    atc_code = DrugAtcAssociation.objects.filter(drug_id=drug).values_list('atc_id_id')
    context["atc_code"] = atc_code
    # context["num_substance"] = len(atc_code)
    context["num_substance"] = 14
    # num_list = [num + 1 for num in range(len(atc_code))]
    num_list = [num + 1 for num in range(14)]
    context ['num_list'] = num_list


    # # Retrieve the related ATC codes in 5 levels
    # atc_chemical_substance = AtcChemicalSubstance.objects.get(id=atc_code.id[:7])
    # atc_chemical_group = AtcChemicalGroup.objects.get(id=atc_code.id[:5])
    # atc_pharmacological_group = AtcPharmacologicalGroup.objects.get(id=atc_code.id[:4])
    # atc_therapeutic_group = AtcTherapeuticGroup.objects.get(id=atc_code.id[:3])
    # atc_anatomical_group = AtcAnatomicalGroup.objects.get(id=atc_code.id[:1])

    # print("atc_chemical_substance = ", atc_chemical_substance)
    # print("atc_chemical_group = ", atc_chemical_group)
    # print("atc_pharmacological_group = ", atc_pharmacological_group)
    # print("atc_therapeutic_group = ", atc_therapeutic_group)
    # print("atc_anatomical_group = ", atc_anatomical_group)


    # # Retrieve the drugs that belong to each ATC code level
    # atc_chemical_substance_drugs = DrugAtcAssociation.objects.filter(atc_id__id__startswith=atc_chemical_substance.id).values_list('drug_id__name', flat=True)
    # atc_pharmacological_group_drugs = DrugAtcAssociation.objects.filter(atc_id__id__startswith=atc_pharmacological_group.id).values_list('drug_id__name', flat=True)
    # atc_therapeutic_group_drugs = DrugAtcAssociation.objects.filter(atc_id__id__startswith=atc_therapeutic_group.id).values_list('drug_id__name', flat=True)
    # atc_anatomical_group_drugs = DrugAtcAssociation.objects.filter(atc_id__id__startswith=atc_anatomical_group.id).values_list('drug_id__name', flat=True)


    # # Print the results
    # print(f"Related ATC code of drug {drug_name}: {atc_code}")
    # print(f"ATC Chemical Substance: {atc_chemical_substance}")
    # print(f"Drugs in ATC Chemical Substance: {atc_chemical_substance_drugs}")
    # print(f"ATC Pharmacological Group: {atc_pharmacological_group}")
    # print(f"Drugs in ATC Pharmacological Group: {atc_pharmacological_group_drugs}")
    # print(f"ATC Therapeutic Group: {atc_therapeutic_group}")
    # print(f"Drugs in ATC Therapeutic Group: {atc_therapeutic_group_drugs}")
    # print(f"ATC Anatomical Group: {atc_anatomical_group}")
    # print(f"Drugs in ATC Anatomical Group: {atc_anatomical_group_drugs}")
    print("atc_code: ", atc_code)
    print("context ", context)

    return render(request, 'draft_drug_atc_tabs.html', context)