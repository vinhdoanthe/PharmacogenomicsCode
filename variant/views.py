from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import GenebassVariant


def get_genebass_tables(request):
    """Get the genebass tables for a variant.
    """
    variant_marker = request.GET.get("variant_marker")
    list_genebass = GenebassVariant.objects.filter(markerID=variant_marker)
    html = render_to_string(
        template_name="variant/genebass_tables.html",
        context={
            "list_genebass": list_genebass,
        },
        request=request,
    )

    return HttpResponse(html)
