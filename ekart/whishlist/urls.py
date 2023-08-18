
from django.urls import path
from .import views

urlpatterns = [
    path("", views.whishlist_view, name='whishlist_view'),
    path("add_to_whishlist/<int:prod_id>/", views.add_to_whishlist, name='add_to_whishlist'), 
    path("item_remove/<int:item_id>/", views.witem_remove, name='witem_remove'),
]
