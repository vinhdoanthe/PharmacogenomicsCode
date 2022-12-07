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


from protein.models import Protein


# Create your views here.


class ProteinBrowser(TemplateView):

    template_name = 'protein_browser.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        browser_columns = ["uniprot_ID", "genename",
                           "geneID", "entry_name", "protein_name"]

        table = pd.DataFrame(columns=browser_columns)
        # receptor_id
        protein_data = Protein.objects.all().values_list(
            "uniprot_ID",
            "genename",
            "geneID",
            "entry_name",
            "protein_name"
        ).distinct()

        for data in protein_data:

            data_subset = {}
            data_subset['uniprot_ID'] = data[0].replace('Class ', '')
            data_subset['genename'] = data[1]
            data_subset['geneID'] = data[2]
            data_subset['entry_name'] = data[3]
            data_subset['protein_name'] = data[4]

            table = table.append(data_subset, ignore_index=True)

        table.fillna('', inplace=True)
        # context = dict()
        context['Array'] = table.to_numpy()
        return context
