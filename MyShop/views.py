from django.shortcuts import render

# Create your views here.
from MyShop.models import Category,Product

def home(request):
    prod_list = Product.objects.order_by('-name')
    print(prod_list)
    return render(request,'MyShop/index.html',{'products':prod_list})

def details(request,pid):
    print(pid)
    prod_list = Product.objects.all()
    found = False
    for prod in prod_list:
        if prod.pid == pid:
            found = True
            return render(request,'MyShop/details.html',{'product':prod,})
    if not found:
        return render(request,'MyShop/details.html',{'product':None,})
