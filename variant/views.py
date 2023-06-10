from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import (
    GenebassVariant,
    Variant,
    VepVariant,
)


def get_genebass_tables(request):
    """Get the genebass tables for a variant.
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
        'gb_id',
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
