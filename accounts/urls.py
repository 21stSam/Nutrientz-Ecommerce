from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # The login page uses your branded template
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # The 'Traffic Controller' address
    path('login-success/', views.login_success, name='login_success'),

    # Make sure this name matches the one in your base.html {% url %} tag
    path('register/', views.register, name='register'), 
    ]