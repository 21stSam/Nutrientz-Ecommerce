from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('callback/', views.payment_callback, name='payment_callback'), # <--- This line caused the error
    path('retry/<int:order_id>/', views.order_retry_payment, name='order_retry_payment'),
    path('my-orders/', views.user_order_history, name='user_order_history'),
    path('dashboard/', views.merchant_dashboard, name='merchant_dashboard'),
    path('merchant/dashboard/', views.merchant_dashboard, name='merchant_dashboard'),
  
]