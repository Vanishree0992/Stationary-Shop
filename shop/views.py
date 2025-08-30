from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Product, Category
from django.views.decorators.http import require_POST


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True, image__isnull=False)  # Added image filter
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        template_name = f"shop/{category.slug}.html"
    else:
        template_name = "shop/product_list.html"
    
    context = {
        "categories": categories,
        "category": category,
        "products": products,
    }
    return render(request, template_name, context)

def add_to_cart(request):
    """Add a product to the cart."""
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))

        product = get_object_or_404(Product, id=product_id)

        cart = request.session.get("cart", {})

        if str(product_id) in cart:
            cart[str(product_id)]["quantity"] += quantity
        else:
            cart[str(product_id)] = {
                "name": product.name,
                "price": float(product.price),
                "quantity": quantity,
                "image": product.image.url if product.image else "",  # ✅ store image
            }

        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request, f"{product.name} added to cart.")
        return redirect("shop:cart")

    return redirect("shop:product_list")


def cart_view(request):
    """Display cart contents."""
    cart = request.session.get("cart", {})
    items, total = [], Decimal("0.00")

    for pid, data in cart.items():
        price = Decimal(data["price"])
        qty = data["quantity"]
        subtotal = price * qty
        total += subtotal
        items.append({
            "product_id": pid,
            "name": data["name"],
            "image": data.get("image", ""),   # ✅ safe image fetch
            "price": price,
            "quantity": qty,
            "subtotal": subtotal,
        })

    return render(request, "shop/cart.html", {"items": items, "total": total})

@require_POST
def update_cart(request, product_id):
    """Increase or decrease product quantity in cart."""
    cart = request.session.get("cart", {})
    action = request.POST.get("action")

    if str(product_id) in cart:
        if action == "increase":
            cart[str(product_id)]["quantity"] += 1
        elif action == "decrease" and cart[str(product_id)]["quantity"] > 1:
            cart[str(product_id)]["quantity"] -= 1

    request.session["cart"] = cart
    request.session.modified = True
    return redirect("shop:cart")



def remove_from_cart(request, product_id):
    """Remove a single product from the cart."""
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session["cart"] = cart
        request.session.modified = True
        messages.info(request, "Item removed from cart.")
    return redirect("shop:cart")


def clear_cart(request):
    """Clear the entire cart."""
    request.session["cart"] = {}
    request.session.modified = True
    messages.info(request, "Cart cleared.")
    return redirect("shop:cart")


def checkout_view(request):
    """Simple checkout page."""
    cart = request.session.get("cart", {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect("shop:product_list")

    items, total = [], Decimal("0.00")
    for pid, data in cart.items():
        price = Decimal(data["price"])
        qty = data["quantity"]
        subtotal = price * qty
        total += subtotal
        items.append({
            "product_id": pid,
            "name": data["name"],
            "image": data.get("image", ""),   # ✅ safe image fetch
            "price": price,
            "quantity": qty,
            "subtotal": subtotal,
        })

    return render(request, "shop/checkout.html", {"items": items, "total": total})