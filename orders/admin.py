from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product'] # Makes searching for products easier in a large inventory
    extra = 0 # Prevents empty rows from cluttering the view

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email', 
        'status', 'total_paid', 'created'
    ]
    list_filter = ['status', 'created', 'updated']
    inlines = [OrderItemInline]

    # Custom Action for your Demo
    actions = ['make_paid']

    @admin.action(description='Mark selected orders as Paid')
    def make_paid(self, request, queryset):
        queryset.update(status='paid')