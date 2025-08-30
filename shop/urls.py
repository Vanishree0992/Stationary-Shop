from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.product_list, name="product_list"),  # all products (default)
    path("category/<slug:category_slug>/", views.product_list, name="product_list_by_category"),  # category pages
    path("cart/", views.cart_view, name="cart"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("clear-cart/", views.clear_cart, name="clear_cart"),
     path("update/<int:product_id>/", views.update_cart, name="update_cart"),
]
