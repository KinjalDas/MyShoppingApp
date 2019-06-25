from MyShop.models import *
from MyAccounts.models import *
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
# Create your views here.

try:
    from django.contrib.sessions.models import Session
    Session.objects.all().delete()
    for carts in Cart.objects.all():
        carts.delete()
    for product_pair in ProductPair.objects.all():
        product_pair.delete()
except:
     pass

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
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment;filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response,pagesize = A4)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(270,500, "Hello world.")
    p.linkURL('/', (270,500,330,510), relative=1)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
