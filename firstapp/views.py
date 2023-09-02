from django.shortcuts import render, redirect
from .models import Product, CartItem, Vendor
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import vendor_required
import requests, json
from django.http import JsonResponse
from http import HTTPStatus

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_vendor:
                Vendor.objects.create(user=user)
            return redirect('firstapp:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'firstapp/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('firstapp:profile')
        else:
            # Handle invalid login
            pass
    return render(request, 'firstapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('firstapp:product_list')


def product_list(request):
    response = requests.get('http://127.0.0.1:8000/api/get_products')
    response_content = response.content
    data = json.loads(response_content)

    if response.status_code == HTTPStatus.OK:
        return render(request, 'firstapp/product_list.html', {'products': data})
    else:
        return JsonResponse(data, status=response.status_code)


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'firstapp/product_detail.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('firstapp:product_list')


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    amount = 0
    for item in cart_items:
        amount += item.product.price * item.quantity
    return render(request, 'firstapp/cart.html', {'cart_items': cart_items, 'amount': amount})


def remove_cart(request, pk):
    cart_item = CartItem.objects.get(id=pk)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('firstapp:cart')


@login_required
def profile(request):
    if request.user.is_vendor:
        # Render vendor profile template
        return render(request, 'firstapp/vendor_profile.html')
    else:
        # Render customer profile template
        return render(request, 'firstapp/customer_profile.html')


#   vendors functions

@login_required
@vendor_required
def vendor_dashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    products = Product.objects.filter(vendor=vendor)
    return render(request, 'firstapp/vendor_dashboard.html', {'products': products})

@login_required
@vendor_required
def add_product(request):
    if request.method == 'POST':
        # import pdb
        # pdb.set_trace()
        vendor = Vendor.objects.get(user=request.user)
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES['image']
        data = {'vendor': vendor.pk, 'name': name, 'description': description, 'price': price}
        # product = Product.objects.create(vendor=vendor, name=name, description=description, price=price, image=image)

        response = requests.post('http://127.0.0.1:8000/api/add_product/', data=data, files=request.FILES)
        response_content = response.content
        data = json.loads(response_content)

        if response.status_code == HTTPStatus.CREATED:
            return redirect('firstapp:vendor_dashboard')
        else:
            return JsonResponse(data)
    return render(request, 'firstapp/add_product.html')

@login_required
@vendor_required
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('firstapp:vendor_dashboard')
    return render(request, 'firstapp/edit_product.html', {'product': product})


@login_required
@vendor_required
def delete_product(request, product_id):
    if request.method == 'POST':
        response = requests.delete('http://127.0.0.1:8000/api/delete_product/' + str(product_id))
        # response_content = response.content
        # data = json.loads(response_content)
        if response.status_code == HTTPStatus.OK:
            return redirect('firstapp:vendor_dashboard')
        # else: 
        #     return JsonResponse(data, status=response.status_code)
    return render(request, 'firstapp/delete_product.html')