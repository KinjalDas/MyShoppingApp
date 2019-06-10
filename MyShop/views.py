from django.shortcuts import render

# Create your views here.
from MyShop.models import Category,Product

def home(request):
    prod_list = Product.objects.order_by('-name')
    return render(request,'MyShop/index.html',{'products':prod_list})

def details(request,pid):
    return render(request,'MyShop/details.html',{'pid':pid,})
