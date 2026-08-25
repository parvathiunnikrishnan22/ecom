from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *


# Home page
def shopfn(request):

    z = Product.objects.all()

    return render(
        request,
        'home.html',
        {'ab': z}
    )


# Customer page
def customerfn(request):

    z = Customer.objects.all()

    return render(
        request,
        'customer.html',
        {'ab': z}
    )


# Order page
def orderfn(request):

    z = Order.objects.all()

    return render(
        request,
        'order.html',
        {'ab': z}
    )


# Order Item page
def orderitemfn(request):

    z = OrderItem.objects.all()

    return render(
        request,
        'orderitem.html',
        {'ab': z}
    )


# Add product to cart
@login_required
def addcartfn(request, pid):

    product = Product.objects.get(id=pid)

    customer = Customer.objects.get(
        email=request.user.email
    )

    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:
        item.quantity = 1
    else:
        item.quantity = item.quantity + 1

    item.save()

    return redirect('/cartview/')
# View cart
@login_required
def cartviewfn(request):

    customer = Customer.objects.get(
        email=request.user.email
    )

    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    items = CartItem.objects.filter(
        cart=cart
    )

    total = 0

    for item in items:

        total = total + (
            item.product.price * item.quantity
        )

    return render(
        request,
        'cart.html',
        {
            'items': items,
            'total': total
        }
    )


# Update quantity
@login_required
def updatecartfn(request, pid):

    customer = Customer.objects.get(
        email=request.user.email
    )

    item = CartItem.objects.get(
        id=pid,
        cart__customer=customer
    )

    quantity = int(
        request.POST.get('quantity')
    )

    if quantity > 0:

        item.quantity = quantity
        item.save()

    return redirect('cartview')


# Remove product from cart
@login_required
def removecartfn(request, pid):

    customer = Customer.objects.get(
        email=request.user.email
    )

    item = CartItem.objects.get(
        id=pid,
        cart__customer=customer
    )

    item.delete()

    return redirect('cart')

    
def loginfn(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

    return render(request, 'login.html')


