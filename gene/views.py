import decimal
import hashlib
import itertools
import json
import random
import re
import time

import numpy as np
import pandas as pd
import urllib

from random import SystemRandom
from copy import deepcopy
from collections import defaultdict, OrderedDict

from django.db.models.functions import Cast
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, DetailView

from django.db.models import Q, Count, Subquery, OuterRef, IntegerField, F
from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache

from gene.forms import FilterForm
from variant.models import Variant, VepVariant, GenebassVariant, VariantPhenocode
from gene.models import Gene

from django.views.generic import ListView


class GeneDetailBrowser(TemplateView):

    template_name = 'gene_detail.html'

    browser_columns = [
        "Variant_marker",  # MarkerID
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

    list_necessary_columns = [
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

    name_dic = {'NMD': 'NMD_transcript', 'cse': 'coding_sequence', 'fsh': 'frameshift',
                'itc': 'incomplete_terminal_codon', 'ide': 'inframe_deletion', 'iis': 'inframe_insertion',
                'mis': 'missense', 'pal': 'protein_altering', 'sac': 'splice_acceptor', 'sdo': 'splice_donor',
                'sd5': 'splice_donor_5th_base', 'sdr': 'splice_donor_region',
                'spt': 'splice_polypyrimidine_tract', 'sre': 'splice_region', '_sl': 'start_lost',
                '_sr': 'start_retained', 'sga': 'stop_gained', 'sl_': 'stop_lost', 'sr_': 'stop_retained',
                'syn': 'synonymous', 'H': 'high', 'M': 'Medium', 'L': 'Low'}

    def parse_marker_data(self, marker, vep_score):
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

        return data_subset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')

        if slug is not None:
            if cache.get("variant_data_" + slug) is not None:
                table_with_protein_pos_int = cache.get("variant_data_" + slug)
                print("Cache hit")
            else:
                browser_columns = self.browser_columns

                table = pd.DataFrame(columns=browser_columns)

                # Retrieve all variant markers from a gene
                if slug.startswith("ENSG"):
                    marker_ID_data = Variant.objects.filter(Gene_ID=slug).values_list(
                        "VariantMarker")

                else:
                    geneid = Gene.objects.filter(genename=slug).values_list("gene_id")[0][0]
                    marker_ID_data = Variant.objects.filter(Gene_ID=geneid).values_list(
                        "VariantMarker")

                # Below code should be rewritten to avoid N+1 queries
                for marker in marker_ID_data:
                    # Retrieve all VEP scores for each variant marker
                    vep_scores = VepVariant.objects.filter(
                        Variant_marker=marker).exclude(Protein_position__icontains='-').values_list(*self.list_necessary_columns)
                    for vep_score in vep_scores:
                        data_subset = self.parse_marker_data(marker, vep_score)
                        table = table.append(data_subset, ignore_index=True)

                table.fillna('', inplace=True)

                context = dict()

                table_with_mean_vep_score = []
                for data_row in table.to_numpy():
                    try:
                        cleaned_values = [x for x in data_row[10:] if str(x) != '']
                        if len(cleaned_values) != 0:
                            mean_vep_score = np.mean(cleaned_values)
                            table_with_mean_vep_score.append(np.append(data_row, mean_vep_score))
                    except Exception as e:
                        print("Error in calculating mean VEP score {0}".format(data_row[10:]))
                        print("-------------------")
                        print(e)
                table_with_protein_pos_int = []
                for data_row in table_with_mean_vep_score:
                    try:
                        data_row[5] = int(data_row[5])
                        table_with_protein_pos_int.append(data_row)
                    except Exception as e:
                        print("Error in converting protein position to int {0}".format(data_row[5]))
                        print("-------------------")
                        print(e)

                cache.set("variant_data_" + slug, table_with_protein_pos_int, 60 * 60)

            context['array'] = table_with_protein_pos_int
            context['length'] = len(table_with_protein_pos_int)
            context["name_dic"] = self.name_dic

            # Mean of Vep scores form
            filter_form = FilterForm()

            context['filter_form'] = filter_form
            context['gene'] = Gene.objects.filter(gene_id=slug).first()

            transcripts = [item[1] for item in table_with_protein_pos_int]
            context['transcripts'] = list(set(transcripts))
            variants = [item[0] for item in table_with_protein_pos_int]
            context['variants'] = list(set(variants))

            consequences = []
            for item in table_with_protein_pos_int:
                coseq = item[2].split(",")
                if len(coseq) >= 1:
                    consequences += coseq

            context['consequences'] = list(set(consequences))

            print(f"transcripts: {len(context['transcripts'])} {context['transcripts']}")
            print(f"variants: {len(context['variants'])}")
            print(f"consequences: {len(context['consequences'])} {context['consequences']}")

        return context


class genebassVariantListView(TemplateView):
    template_name = "genebass/variant_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        genebass_variants_list = GenebassVariant.objects.filter(  # Filter to get all genebass variants for a gene
            markerID__in=Variant.objects.filter(  # Filter to get all variants for a gene
                Gene_ID=self.kwargs['pk']  # Gen Gene by gene_id
            ).values_list('VariantMarker', flat=True)
        ).values(
            'markerID__VariantMarker',
            'n_cases',
            'n_controls',
            'phenocode__description',
            'phenocode',
            'n_cases_defined',
            'n_cases_both_sexes',
            'n_cases_females',
            'n_cases_males',
            'category',
            'AC',
            'AF',
            'BETA',
            'SE',
            'AF_Cases',
            'AF_Controls',
            'Pvalue',
        )

        print(f"genebass_variants_list count: {genebass_variants_list.count()}")

        genebass_variants_list = genebass_variants_list[:5000]

        phenotypes = GenebassVariant.objects.filter(  # Filter to get all genebass variants for a gene
            markerID__in=Variant.objects.filter(  # Filter to get all variants for a gene
                Gene_ID=self.kwargs['pk']  # Gen Gene by gene_id
            ).values_list('VariantMarker', flat=True)
        ).values_list('phenocode', flat=True).distinct()

        # đổi lại câu query để lấy categories
        categories = GenebassVariant.objects.filter(  # Filter to get all genebass variants for a gene
            markerID__in=Variant.objects.filter(  # Filter to get all variants for a gene
                Gene_ID=self.kwargs['pk']  # Gen Gene by gene_id
            ).values_list('VariantMarker', flat=True)
        ).values_list('category', flat=True).distinct()

        context['gene'] = Gene.objects.get(pk=self.kwargs['pk'])
        context['variant_list'] = genebass_variants_list
        context['phenotypes'] = phenotypes
        context['categories'] = categories

        return context


@require_http_methods(["GET"])
def filter_gene_detail_page(request, id):
    """
    Filter gene detail page by
    * mean_of_vep_score
    """
    mean_vep_score = request.GET.get('mean_vep_score', 0.5)
    mean_vep_score = float(mean_vep_score)
    # Filter by mean_vep_score
    list_vep_variants = VepVariant.objects.filter(Variant_marker__in=Variant.objects.filter(Gene_ID=id).values_list('VariantMarker',
                                                                                                flat=True)
                              ).exclude(Protein_position__contains="-").annotate(
                                                                            protein_pos_int=Cast('Protein_position', IntegerField()),
                                                                            mean_vep_score=(F('BayesDel_addAF_rankscore') + F('BayesDel_noAF_rankscore')) / 2
    ).filter(mean_vep_score__gte=mean_vep_score).exclude(mean_vep_score=decimal.Decimal('NaN')).order_by('protein_pos_int')

    return None


@require_http_methods(["GET"])
def genebass_variants(request):
    """
    Return a list of genebass variants by variant_id
    """
    variant_id = request.GET.get('variant_id', None)
    if variant_id:
        pass
        # TODO: Filter genebass variants by variant_id
    else:
        return HttpResponseBadRequest()