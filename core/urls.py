from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name='home'),
    path("shop/", views.shop, name="shop"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path("my-order/", views.my_order, name="my_order"),
    path("track-order/", views.track_order, name="track_order"),
    path("search/", views.search, name="search"),
]
