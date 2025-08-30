from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, "core/home.html")

# ✅ Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("core:home")
        else:
            messages.error(request, "Invalid username or password")
    return redirect("core:home")   # stays on home with modal

# ✅ Register View
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("core:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("core:register")

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created! Please log in.")
        return redirect("core:home")   # ✅ After register → back to home

    return render(request, "core/register.html")

# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect("core:home")


def home(request):
    return render(request, "core/home.html")

def shop(request):
    return render(request, "core/shop.html")

def about(request):
    return render(request, "core/about.html")

def contact(request):
    return render(request, "core/contact.html")

def cart(request):
    return render(request, "core/cart.html")

def my_order(request):
    # For now, just render a template
    return render(request, "core/myorder.html")

def track_order(request):
    # For now, just render a template
    return render(request, "core/track.html")

def search(request):
    query = request.GET.get("q", "")
    # later we can connect this to a Product model
    context = {"query": query, "results": []}
    return render(request, "core/search.html", context)
