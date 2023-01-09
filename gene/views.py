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


from variantmarker.models import VariantMarker
from variantphenocode.models import VariantPhenocode
from vep.models import Vep
from gene.models import Gene
from gbvariant.models import GenebassVariant
from django.views.generic import ListView

# Create your views here.


class GeneBrowser(TemplateView):

    # template_name = 'gene_browser.html'
    template_name = 'gene_browser_copy.html'
    # template_name = 'heatmap-plotly.html'
    # template_name = "connected-graph.html"
    # template_name = "connected-graph-plotly.html"
    # template_name = 'consequence_piechart.html'
    # paginate_by = 20

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        browser_columns = ["Variant",  # MarkerID
                           "Source",
                           "cDNA_position",
                           "CDS_position",
                           "protein_position",
                           "amino_acids",
                           "codons",
                           "consequence",
                           "impact",
                           "phenocode",
                           "SIFT",
                           "Polyphen2_HDIV",
                           "Polyphen2_HVAR",
                           "FATHMM",
                           "DEOGEN2",
                           ]

        table = pd.DataFrame(columns=browser_columns)

        # Retrieve all variant markers from a gene
        marker_ID_data = VariantMarker.objects.filter(geneID='ENSG00000170989').values_list(
            "markerID")

        for marker in marker_ID_data:
            # Retrieve all VEP scores for each variant marker
            vep_scores = Vep.objects.filter(
                markerID=marker).values_list("cDNA_position",
                                             "CDS_position",
                                             "protein_position",
                                             "amino_acids",
                                             "codons",
                                             "consequence",
                                             "impact",
                                             "SIFT_score",
                                             "Polyphen2_HDIV_score",
                                             "Polyphen2_HVAR_score",
                                             "FATHMM_score",
                                             "DEOGEN2_score")
            for vep_score in vep_scores:
                data_subset = {}

                # Retrieve phenocode
                # Phenocode data is now not fully load --> this is just for the code runs
                err = False
                try:
                    phenocode = GenebassVariant.objects.filter(
                        markerID=marker).values_list("phenocode")[0][0]
                except:
                    err = True

                if err:
                    phenocode = 1000000

                data_subset["phenocode"] = phenocode

                data_subset["Variant"] = marker
                data_subset["Source"] = "Ensemble"
                data_subset["cDNA_position"] = vep_score[0]
                data_subset["CDS_position"] = vep_score[1]
                data_subset["protein_position"] = vep_score[2]
                data_subset["amino_acids"] = vep_score[3]
                data_subset["codons"] = vep_score[4]
                data_subset["consequence"] = vep_score[5]
                data_subset["impact"] = vep_score[6]
                data_subset["SIFT"] = vep_score[7]
                data_subset["Polyphen2_HDIV"] = vep_score[8]
                data_subset["Polyphen2_HVAR"] = vep_score[9]
                data_subset["FATHMM"] = vep_score[10]
                data_subset["DEOGEN2"] = vep_score[11]

                table = table.append(data_subset, ignore_index=True)

        table.fillna('', inplace=True)
        length = len(table)
        
        consequence_dict = {}
        for i in range(length):
            values = table["consequence"][i].split(",")
            for value in values:
                consequence_dict[value] = consequence_dict.get(value, 0)+1

        # context = dict()
        print(table.head(3))
        print("*************** ", consequence_dict)
        context['Array'] = table.to_numpy()
        context['length'] = length
        for key in consequence_dict.keys():
            context[key] = consequence_dict.get(key)
        print("************ Type of array ", type(context['Array']))
        print("************ Elements of array ", context['Array'][:5])
        # context["qs"] = Editors.objects.all()
        context["consequence_dict"] = consequence_dict
        return context
