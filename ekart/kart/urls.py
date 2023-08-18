
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path("", views.home, name='home'),
    path("add_to_cart/<int:prod_id>/", views.add_to_cart, name='add_to_cart'),
    path("cart_view/", views.cart_view, name='cart_view'),
    path("cart_view/increase/<int:item_id>/", views.cart_increase, name='increase'),
    path("cart_view/decrease/<int:item_id>/", views.cart_decrease, name='decrease'),
    path("cart_view/item_remove/<int:item_id>/", views.item_remove, name='item_remove'),
]
