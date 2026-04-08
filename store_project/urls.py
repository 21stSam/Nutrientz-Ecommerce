from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from django.conf import settings
from django.conf.urls.static import static

# --- Add these lines to style the Admin ---
admin.site.site_header = "Nutrientz Merchant Admin"
admin.site.site_title = "Starling ERP"
admin.site.index_title = "Mission Control"
# ------------------------------------------

urlpatterns = [
    path("admin/", admin.site.urls),
    # Move specific apps to the top
    path("cart/", include("cart.urls", namespace="cart")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    # Put the shop (root) at the very bottom
    path("", include("shop.urls", namespace="shop")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
