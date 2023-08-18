
from django.urls import path
from .import views

urlpatterns = [
    path("place_order", views.checkout, name='checkout'),
    path("payments/",views.payments,name='payments'), 
    path("order_complete/",views.order_complete,name='order_complete'), 
]
