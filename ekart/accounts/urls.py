
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path("signup/", views.register_user, name='register_user'),
    path("login/", views.login_user, name='login_user'),
    path("verify_user/", views.verify_user, name='verify_user'),
    path("logout/", views.logout_user, name='logout_user'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("my_orders/", views.my_orders, name='my_orders'),
    path("edit_profile/", views.edit_profile, name='edit_profile'),
    path("change_password/", views.change_password, name='change_password'),
    path("forgotpassword/", views.forgotpassword, name='forgotpassword'),
    path("reset_password/", views.reset_password, name='reset_password'),
    path("order_detail/<int:order_id>", views.order_detail, name='order_detail'),
    path("user_feedback/", views.user_feedback, name='user_feedback'),
]
