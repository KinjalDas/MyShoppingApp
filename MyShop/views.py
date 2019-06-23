from MyShop.models import *
from django.shortcuts import render
# Create your views here.

from django.contrib.sessions.models import Session
Session.objects.all().delete()
for carts in Cart.objects.all():
    carts.delete()
for product_pair in ProductPair.objects.all():
    product_pair.delete()


def check_cart(request):
    if request.session.get("cart") == None:
        cart=Cart()
        cart.save()
        request.session["cart"] = cart.id


def home(request,registered=False,user=None):
    check_cart(request)
    print(request.session["cart"])
    prod_list = Product.objects.order_by('-name')
    print(prod_list)
    return render(request,'MyShop/index.html',{'products':prod_list,'registered':registered,'user':user})

def details(request,pid):
    check_cart(request)
    print(request.session["cart"])
    print(pid)
    try:
        prod = Product.objects.get(pid = pid)
        print(prod)
        return render(request,'MyShop/details.html',{'product':prod,})
    except:
        return render(request,'MyShop/details.html',{'product':None,})

def category(request,Category):
    check_cart(request)
    print(request.session["cart"])
    prod_list = Product.objects.all()
    found = False
    prods = []
    for prod in prod_list:
        if prod.category.name == Category:
            found = True
            prods.append(prod)
    return render(request,'MyShop/category.html',{'products':prods,'found':found})

def view_cart(request):
    check_cart(request)
    print(request.session["cart"])
    carts = Cart.objects.get(id = request.session["cart"])
    prod_pairs=[]
    if len(carts.products.all()) == 0:
        return render(request,'MyShop/cart.html',{'cart':False,})
    else:
        prod_pairs = carts.products.all()
        for prod_pair in prod_pairs:
            print(prod_pair.product.name,prod_pair.shop_quant)
        return render(request,'MyShop/cart.html',{'cart':True,'prod_pairs':prod_pairs,})

def add_to_cart(request,id,quant):
    check_cart(request)
    print(request.session["cart"])
    cart = Cart.objects.get(id = request.session["cart"])
    prod_pairs = cart.products.all()
    for prod in prod_pairs:
        if prod.product.pid == id:
            prod.shop_quant += quant
            prod.save()
            return view_cart(request)
    product = Product.objects.get(pid = id)
    prod_pair = ProductPair(product = product,shop_quant = quant)
    prod_pair.save()
    cart.products.add(prod_pair)
    cart.save()
    print(cart)
    return view_cart(request)

def remove_from_cart(request,id):
    check_cart(request)
    print(request.session["cart"])
    cart = Cart.objects.get(id = request.session["cart"])
    for prod_pair in cart.products.all():
        if prod_pair.product.pid == id:
            print("try to remove"+ prod_pair.product.name + str(id))
            cart.products.remove(prod_pair)
            print(prod_pair.product.name + "removed")
    #try:
    return view_cart(request)
    #except:
    #    return view_cart(request)
