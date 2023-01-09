from django.views.generic import ListView, TemplateView
from interaction.models import Interaction
from drug.models import Drug
from protein.models import Protein
from variantmarker.models import VariantMarker
import pandas as pd
from django.core.paginator import Paginator

# Create your views here.


class DrugPaginationBrowser(ListView):

    template_name = 'drug_pagination_browser.html'
    paginate_by = 3
    model = Interaction

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
            drug_bankID='DB00002').values_list("drugtype")

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
            data_subset["#variants"] = len(markers)

            table = table.append(data_subset, ignore_index=True)

        table.fillna('', inplace=True)
        # context = dict()
        print(table.head(3))
        print("--------------------  drug_data[0][0]: ", drug_data[0][0])

        items = table.to_numpy()
        p = Paginator(items, 2)
        print("Number of pages = ", p.num_pages)
        page = p.page(1)
        print("page page page page page = ", page)
        print("page page page page page type = ", type(page))
        context['first_page'] = page
        context['pages'] = p
        return context
