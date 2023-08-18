from django.urls import path
from .import views

urlpatterns = [
    path("", views.store, name='store'),
    path("search/", views.search, name='search'),
    path("category/<slug:type>/", views.category_sort, name='category_sort'),
    path("product_view/<int:prod_id>/", views.product_view, name='product_view'),
]
