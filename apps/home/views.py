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


class Home(TemplateView):

    template_name = 'index_pharmcodb.html'
    context = {}



def drug_target_network(request):
    context = {'message': 'Hello from drug_and_target_network.html page!'}
    return render(request, 'home/drug_and_target_network.html', context)
    # return render(request, 'home/drug_and_target_network copy.html', context)
