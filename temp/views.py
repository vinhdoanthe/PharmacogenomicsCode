from django.shortcuts import render

# Create your views here.
from .models import Order 

def index(request):
    orders = Order.objects.all()
    for order in orders:
        temp = order
    
    return render(request, "index.html")


