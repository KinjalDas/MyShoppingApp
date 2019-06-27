from MyShop.models import *
from MyAccounts.models import *
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.db.utils import ProgrammingError

from django.http import HttpResponse
from django.template.loader import render_to_string
import tempfile
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.

try:
    Session.objects.all().delete()
    for carts in Cart.objects.all():
        carts.delete()
    for product_pair in ProductPair.objects.all():
        product_pair.delete()
except ProgrammingError:
     print("first run")

def check_cart(request):
    if not request.session.get("cart"):
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
            ProductPair.objects.filter(product = prod_pair.product).delete()
            print(prod_pair.product.name + "removed")
            return view_cart(request)
    return view_cart(request)

def update_cart(request,id):
    check_cart(request)
    print(request.session["cart"])
    cart = Cart.objects.get(id = request.session["cart"])
    if request.method == "POST":
        for prod_pair in cart.products.all():
            if prod_pair.product.pid == id:
                prod_pair.shop_quant = request.POST["quantity"]
                prod_pair.save()
    return view_cart(request)

@login_required
def checkout(request):
    check_cart(request)
    user_prof = UserProfile.objects.get(user = User.objects.get(username = request.session["username"]))
    print(user_prof)
    cart = Cart.objects.get(id = request.session["cart"])
    orders = []
    for prod_pair in cart.products.all():
        print(prod_pair.product , prod_pair.shop_quant)
        order = Order(user = user_prof)
        order.product = prod_pair.product
        order.quantity = prod_pair.shop_quant
        prod = Product.objects.get(pid = prod_pair.product.pid)
        prod.quantity -= prod_pair.shop_quant
        prod.save()
        order.save()
        orders.append(order)
        cart.products.remove(prod_pair)
        cart.save()
        ProductPair.objects.filter(product = prod_pair.product).delete()
    return invoice(request,user_prof,orders)

def invoice(request,user_prof,orders):
    template_path = 'MyShop/invoice.html'
    context = {'user_prof':user_prof,'orders':orders}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response
       #, link_callback=link_callback
       )
    # if error then show some funy view
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
