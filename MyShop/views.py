from django.shortcuts import render

# Create your views here.
from MyShop.models import Category,Product

def home(request,registered=False,user=None):
    prod_list = Product.objects.order_by('-name')
    print(prod_list)
    return render(request,'MyShop/index.html',{'products':prod_list,'registered':registered,'user':user})

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

def category(request,Category):
    prod_list = Product.objects.all()
    found = False
    prods = []
    for prod in prod_list:
        if prod.category.name == Category:
            found = True
            prods.append(prod)
    return render(request,'MyShop/category.html',{'products':prods,'found':found})
