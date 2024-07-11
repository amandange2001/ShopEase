from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Category, CartItem
from django.db.models import Q
from random import sample


def index(req):
    products = Product.objects.all()
    random_products = sample(list(products), min(len(products), 3)) 
    return render(req, "index.html", {'random_products': random_products})

def watchbrowse(req):
    if req.user.is_authenticated:
        user = req.user
        # Assuming CartItem model has fields 'user' and 'product'
        user_cart_items = CartItem.objects.filter(user=user)
        product_ids_in_cart = [item.product.id for item in user_cart_items]
        products = Product.objects.exclude(id__in=product_ids_in_cart)
        context = {"username": user.username, "products": products}
        return render(req, "watchbrowse.html", context)
    else:
        products = Product.objects.all()
        context = {"products": products}
        return render(req, "watchbrowse.html", context)


def loginuser(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        upass = request.POST.get("upass")
        context = {}
        
        if not uname or not upass:
            context["errmsg"] = "Fields can't be empty"
            return render(request, "loginuser.html", context)
        else:
            user = authenticate(username=uname, password=upass)
            context["username"] = uname
            
            if user is not None:
                login(request, user)  # This line logs the user in
                return redirect("/")
            else:
                context["errmsg"] = "Invalid username and password"
                return render(request, "loginuser.html", context)
    else:
        return render(request, "loginuser.html")



def registeruser(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        upass = request.POST.get("upass")
        ucpass = request.POST.get("ucpass")
        
        context = {}

        if not uname or not upass or not ucpass:
            context["errmsg"] = "Fields can't be empty"
        elif upass != ucpass:
            context["errmsg"] = "Password and Confirm Password don't match"
        else:
            try:
                user = User.objects.create(username=uname)
                user.set_password(upass)
                user.save()
                return redirect("/loginuser")
            except Exception as e:
                context["errmsg"] = str(e)

        return render(request, "registeruser.html", context)
    else:
        return render(request, "registeruser.html")


def userlogout(req):
    logout(req)
    return redirect("/")

def Gents(req):
    if req.method == "GET": 
        category = Category.objects.get(name='Gents')  
        products = Product.objects.filter(category=category) 
        context = {"products": products}
        return render(req, "watchbrowse.html", context)
    else:
        products = Product.objects.all()
        context = {"products": products}
        return render(req, "watchbrowse.html", context)
    
def Ladies(req):
    if req.method == "GET": 
        category = Category.objects.get(name='Ladies')  
        products = Product.objects.filter(category=category) 
        context = {"products": products}
        return render(req, "watchbrowse.html", context)
    else:
        products = Product.objects.all()
        context = {"products": products}
        return render(req, "watchbrowse.html", context)
    
def Children(req):
    if req.method == "GET": 
        category = Category.objects.get(name='Children')  
        products = Product.objects.filter(category=category) 
        context = {"products": products}
        return render(req, "watchbrowse.html", context)
    else:
        products = Product.objects.all()
        context = {"products": products}
        return render(req, "watchbrowse.html", context)
    
def Couple(req):
    if req.method == "GET": 
        category = Category.objects.get(name='Couple')  
        products = Product.objects.filter(category=category) 
        context = {"products": products}
        return render(req, "watchbrowse.html", context)
    else:
        products = Product.objects.all()
        context = {"products": products}
        return render(req, "watchbrowse.html", context)
    
def searchproduct(req):
    query = req.GET.get("q")
    errmsg = ""
    products = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(category__name__icontains=query) 
        )

        if not products.exists():
            errmsg = "No results found."

    else:
        errmsg = "Please enter a search query."

    context = {"products": products, "query": query, "errmsg": errmsg}
    return render(req, "watchbrowse.html", context)    
    

def buy_product(req, product_id):
    if req.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_id)
        CartItem.objects.create(user=req.user, product=product)
        return redirect('/mycart/') 
    else:
        return redirect('/loginuser/')  
    
@login_required
def mycart(request):
    if request.user.is_authenticated:
        user_cart_items = CartItem.objects.filter(user=request.user)
        total_price = 0
        
        for item in user_cart_items:
            quantity = int(request.POST.get(f"quantity-{item.id}", item.quantity)) 
            item.quantity = quantity
            item.save()  
            item.total_price = item.quantity * item.product.price
            item.save()  
            
            total_price += item.total_price 
        
        context = {"cart_items": user_cart_items, "total_price": total_price}
        return render(request, "mycart.html", context)
    else:
        return redirect('/loginuser/')
    
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    item.delete()
    return redirect('mycart')    

@login_required
def checkout(request):
    user_cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.quantity * item.product.price for item in user_cart_items)
    
    context = {
        'cart_items': user_cart_items,
        'total_price': total_price,
        'user': request.user,
    }
    return render(request, 'checkout.html', context)


   