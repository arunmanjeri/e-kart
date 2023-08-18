
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('kart.urls')),
    path("store/", include('store.urls')),
    path("accounts/", include('accounts.urls')),
    path("whishlist/", include('whishlist.urls')),
    path("checkout/", include('payment.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
