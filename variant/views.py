from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
import numpy as np
import json

from .models import (
    GenebassVariant,
    Variant,
    VepVariant,
)


def get_variant_vep_scores_and_plot(request):
    """
        Get the vep scores for a specific variant
    """
    variant_marker = request.GET.get("variant_marker")

    # Get variant
    try:
        variant = Variant.objects.filter(VariantMarker=variant_marker).first()
    except Variant.DoesNotExist:
        variant = None

    # Get gene
    if variant:
        gene = variant.Gene_ID
    else:
        gene = None

    # Get transcript
    transcript_ids = VepVariant.objects.filter(Variant_marker=variant_marker).values_list('Transcript_ID', flat=True)

    list_vep_scores = VepVariant.objects.filter(Variant_marker=variant_marker).values(
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
                    "LINSIGHT_rankscore",
    )

    vep_scores_data = {
        # DA FIX DE CHAY DUOC VAO DAY. NHUNG HAM DUOI DANG KHONG DUNG, CHUA RO CAN DATA NTN DE VE BOX PLOT
        "x": list(list_vep_scores.keys()),
        "y": [list(scores) for scores in list_vep_scores.values()],
        "type": "box",
        "name": "Variant Scores",
    }

    context = {
        "vep_scores_data": json.dumps(vep_scores_data),
    }

    return render(request, "variant_plot.html", context)




def get_genebass_tables(request):
    """
        Get the genebass tables for a variant.
    """
    variant_marker = request.GET.get("variant_marker")
    # Get variant
    try:
        variant = Variant.objects.filter(VariantMarker=variant_marker).first()
    except Variant.DoesNotExist:
        variant = None

    # Get gene
    if variant:
        gene = variant.Gene_ID
    else:
        gene = None

    # Get transcript
    transcript_ids = VepVariant.objects.filter(Variant_marker=variant_marker).values_list('Transcript_ID', flat=True)

    list_genebass = GenebassVariant.objects.filter(markerID=variant_marker).values(
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

    html = render_to_string(
        template_name="variant/genebass_tables.html",
        context={
            "gene": gene,
            "list_genebass": list_genebass,
            "transcript_ids": transcript_ids,
            "variant": variant,
        },
        request=request,
    )

    return HttpResponse(html)
