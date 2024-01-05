from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Car, CartItem

def Index(request):
    return render(request, "app/homepage.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered")
                return redirect("register")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
                messages.success(
                    request, "Registration successful. You can now log in."
                )
                return redirect("login")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("register")

    return render(request, "app/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "app/login.html")

@login_required(login_url="login")
def homepage(request):
    search_query = request.GET.get("q", "")
    cars = Car.objects.all()

    if search_query:
        cars = cars.filter(model__icontains=search_query)

    context = {
        "cars": cars,
        "search_query": search_query,
    }

    return render(request, "app/homepage.html", context)

@login_required(login_url="login")
def booking_invoice(request, pk):
    car = get_object_or_404(Car, pk=pk)
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(cart_item.car.price_per_hour * cart_item.quantity for cart_item in cart_items)
    if not car.is_rented:
        car.is_rented = True
        car.save()

    context = {
        'car': car,
        'total_price': total_price
    }

    return render(request, 'app/invoice.html', context)

@login_required(login_url="login")
def cartpage(request):
    return render(request, "app/cart.html")

@login_required(login_url="login")
def add_to_cart(request, pk):
    car = get_object_or_404(Car, pk=pk)
    user = request.user
    cart_item, created = CartItem.objects.get_or_create(car=car, user=user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required(login_url="login")
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(cart_item.car.price_per_hour * cart_item.quantity for cart_item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'app/cart.html', context)

@login_required(login_url="login")
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required(login_url="login")
def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login")
