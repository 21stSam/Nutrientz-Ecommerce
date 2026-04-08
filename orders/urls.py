from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    # --- Customer Facing ---
    path("create/", views.order_create, name="order_create"),
    path(
        "retry/<int:order_id>/", views.order_retry_payment, name="order_retry_payment"
    ),
    path("my-orders/", views.user_order_history, name="user_order_history"),
    # --- Payment Integration ---
    path("callback/", views.payment_callback, name="payment_callback"),
    # --- Merchant / Admin (Mission Control) ---
    path("merchant/dashboard/", views.merchant_dashboard, name="merchant_dashboard"),
    path(
        "merchant/order/<int:order_id>/mark-paid/",
        views.mark_order_as_paid,
        name="mark_order_as_paid",
    ),
    path(
        "merchant/order/<int:order_id>/mark-shipped/",
        views.mark_order_as_shipped,
        name="mark_order_as_shipped",
    ),
    path(
        "merchant/order/<int:order_id>/detail/",
        views.merchant_order_detail,
        name="merchant_order_detail",
    ),
]
