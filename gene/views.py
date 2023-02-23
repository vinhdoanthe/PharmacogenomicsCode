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


from variant.models import Variant, VepVariant
from gene.models import Gene

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

        browser_columns = ["Variant_marker",  # MarkerID
                           "Transcript_ID",
                            "Consequence",
                            "cDNA_position",
                            "CDS_position",
                            "Protein_position",
                            "Amino_acids",
                            "Codons",
                            "Impact",
                            "Strand",
                            "BayesDel_addAF_rankscore",
                            "BayesDel_noAF_rankscore",
                            "CADD_raw_rankscore",
                            "ClinPred_rankscore",
                            "DANN_rankscore",
                            "DEOGEN2_rankscore",
                            "Eigen_PC_raw_coding_rankscore",
                            "Eigen_raw_coding_rankscore",
                            "FATHMM_converted_rankscore",
                            "GERP_RS_rankscore",
                            "GM12878_fitCons_rankscore",
                            "GenoCanyon_rankscore",
                            "H1_hESC_fitCons_rankscore",
                            "HUVEC_fitCons_rankscore",
                            "LIST_S2_rankscore",
                            "LRT_converted_rankscore",
                            "M_CAP_rankscore",
                            "MPC_rankscore",
                            "MVP_rankscore",
                            "MetaLR_rankscore",
                            "MetaRNN_rankscore",
                            "MetaSVM_rankscore",
                            "MutPred_rankscore",
                            "MutationAssessor_rankscore",
                            "MutationTaster_converted_rankscore",
                            "PROVEAN_converted_rankscore",
                            "Polyphen2_HDIV_rankscore",
                            "Polyphen2_HVAR_rankscore",
                            "PrimateAI_rankscore",
                            "REVEL_rankscore",
                            "SIFT4G_converted_rankscore",
                            "SIFT_converted_rankscore",
                            "SiPhy_29way_logOdds_rankscore",
                            "VEST4_rankscore",
                            "bStatistic_converted_rankscore",
                            "Fathmm_MKL_coding_rankscore",
                            "Fathmm_XF_coding_rankscore",
                            "Integrated_fitCons_rankscore",
                            "PhastCons30way_mammalian_rankscore",
                            "PhyloP30way_mammalian_rankscore",
                           ]

        table = pd.DataFrame(columns=browser_columns)

        # Retrieve all variant markers from a gene
        marker_ID_data = Variant.objects.filter(Gene_ID='ENSG00000170989').values_list(
            "VariantMarker")

        for marker in marker_ID_data:
            # Retrieve all VEP scores for each variant marker
            vep_scores = VepVariant.objects.filter(
                Variant_marker=marker).values_list("Transcript_ID",
                                                "Consequence",
                                                "cDNA_position",
                                                "CDS_position",
                                                "Protein_position",
                                                "Amino_acids",
                                                "Codons",
                                                "Impact",
                                                "Strand",
                                                "BayesDel_addAF_rankscore",
                                                "BayesDel_noAF_rankscore",
                                                "CADD_raw_rankscore",
                                                "ClinPred_rankscore",
                                                "DANN_rankscore",
                                                "DEOGEN2_rankscore",
                                                "Eigen_PC_raw_coding_rankscore",
                                                "Eigen_raw_coding_rankscore",
                                                "FATHMM_converted_rankscore",
                                                "GERP_RS_rankscore",
                                                "GM12878_fitCons_rankscore",
                                                "GenoCanyon_rankscore",
                                                "H1_hESC_fitCons_rankscore",
                                                "HUVEC_fitCons_rankscore",
                                                "LIST_S2_rankscore",
                                                "LRT_converted_rankscore",
                                                "M_CAP_rankscore",
                                                "MPC_rankscore",
                                                "MVP_rankscore",
                                                "MetaLR_rankscore",
                                                "MetaRNN_rankscore",
                                                "MetaSVM_rankscore",
                                                "MutPred_rankscore",
                                                "MutationAssessor_rankscore",
                                                "MutationTaster_converted_rankscore",
                                                "PROVEAN_converted_rankscore",
                                                "Polyphen2_HDIV_rankscore",
                                                "Polyphen2_HVAR_rankscore",
                                                "PrimateAI_rankscore",
                                                "REVEL_rankscore",
                                                "SIFT4G_converted_rankscore",
                                                "SIFT_converted_rankscore",
                                                "SiPhy_29way_logOdds_rankscore",
                                                "VEST4_rankscore",
                                                "bStatistic_converted_rankscore",
                                                "Fathmm_MKL_coding_rankscore",
                                                "Fathmm_XF_coding_rankscore",
                                                "Integrated_fitCons_rankscore",
                                                "PhastCons30way_mammalian_rankscore",
                                                "PhyloP30way_mammalian_rankscore"
                                                )
            for vep_score in vep_scores:
                data_subset = {}

                data_subset["Variant_marker"] = marker[0]
                data_subset["Transcript_ID"] = vep_score[0]
                data_subset["Consequence"] = vep_score[1]
                data_subset["cDNA_position"] = vep_score[2]
                data_subset["CDS_position"] = vep_score[3]
                data_subset["Protein_position"] = vep_score[4]
                data_subset["Amino_acids"] = vep_score[5]
                data_subset["Codons"] = vep_score[6]
                data_subset["Impact"] = vep_score[7]
                data_subset["Strand"] = vep_score[8]
                data_subset["BayesDel_addAF_rankscore"] = vep_score[9]
                data_subset["BayesDel_noAF_rankscore"] = vep_score[10]
                data_subset["CADD_raw_rankscore"] = vep_score[11]
                data_subset["ClinPred_rankscore"] = vep_score[12]
                data_subset["DANN_rankscore"] = vep_score[13]
                data_subset["DEOGEN2_rankscore"] = vep_score[14]
                data_subset["Eigen_PC_raw_coding_rankscore"] = vep_score[15]
                data_subset["Eigen_raw_coding_rankscore"] = vep_score[16]
                data_subset["FATHMM_converted_rankscore"] = vep_score[17]
                data_subset["GERP_RS_rankscore"] = vep_score[18]
                data_subset["GM12878_fitCons_rankscore"] = vep_score[19]
                data_subset["GenoCanyon_rankscore"] = vep_score[20]
                data_subset["H1_hESC_fitCons_rankscore"] = vep_score[21]
                data_subset["HUVEC_fitCons_rankscore"] = vep_score[22]
                data_subset["LIST_S2_rankscore"] = vep_score[23]
                data_subset["LRT_converted_rankscore"] = vep_score[24]
                data_subset["M_CAP_rankscore"] = vep_score[25]
                data_subset["MPC_rankscore"] = vep_score[26]
                data_subset["MVP_rankscore"] = vep_score[27]
                data_subset["MetaLR_rankscore"] = vep_score[28]
                data_subset["MetaRNN_rankscore"] = vep_score[29]
                data_subset["MetaSVM_rankscore"] = vep_score[30]
                data_subset["MutPred_rankscore"] = vep_score[31]
                data_subset["MutationAssessor_rankscore"] = vep_score[32]
                data_subset["MutationTaster_converted_rankscore"] = vep_score[33]
                data_subset["PROVEAN_converted_rankscore"] = vep_score[34]
                data_subset["Polyphen2_HDIV_rankscore"] = vep_score[35]
                data_subset["Polyphen2_HVAR_rankscore"] = vep_score[36]
                data_subset["PrimateAI_rankscore"] = vep_score[37]
                data_subset["REVEL_rankscore"] = vep_score[38]
                data_subset["SIFT4G_converted_rankscore"] = vep_score[39]
                data_subset["SIFT_converted_rankscore"] = vep_score[40]
                data_subset["SiPhy_29way_logOdds_rankscore"] = vep_score[41]
                data_subset["VEST4_rankscore"] = vep_score[42]
                data_subset["bStatistic_converted_rankscore"] = vep_score[43]
                data_subset["Fathmm_MKL_coding_rankscore"] = vep_score[44]
                data_subset["Fathmm_XF_coding_rankscore"] = vep_score[45]
                data_subset["Integrated_fitCons_rankscore"] = vep_score[46]
                data_subset["PhastCons30way_mammalian_rankscore"] = vep_score[47]
                data_subset["PhyloP30way_mammalian_rankscore"] = vep_score[48]
                # data_subset["LINSIGHT_rankscore"] = vep_score[49]

                table = table.append(data_subset, ignore_index=True)

        table.fillna('', inplace=True)
        length = len(table)
        
        consequence_dict = {}
        for i in range(length):
            values = table["Consequence"][i].split(",")
            for value in values:
                consequence_dict[value] = consequence_dict.get(value, 0)+1

        # context = dict()
        print(table.head(3))
        # print("*************** ", consequence_dict)
        context['array'] = table.to_numpy()
        context['length'] = length
        for key in consequence_dict.keys():
            context[key] = consequence_dict.get(key)
        # print("************ Type of array ", type(context['array']))
        # print("************ Elements of array ", context['array'][:5])
        
        # context["qs"] = Editors.objects.all()
        context["consequence_dict"] = consequence_dict
        return context


#@cache_page(60 * 60 * 24 * 7)
def detail(request, slug):
    # get protein
    slug = slug.upper()

    print("SLUGGGGGGGGGGGGG", slug)
    print("SLUGGGGGGGGGGGGG", slug)
    print("SLUGGGGGGGGGGGGG", slug)
    print("SLUGGGGGGGGGGGGG", slug)
    try:
        if Gene.objects.filter(gene_id=slug).exists():
            p = Gene.objects.get(gene_id=slug)
            print("p --------- ",p)
        
    except:
        context = {'gene_no_found': slug}
        return render(request, 'gene_detail.html', context)

    gene_id = p.gene_id
    genename = p.genename
    context = {'gene_id': gene_id, 'genename': genename}

    return render(request, 'gene_detail.html', context)