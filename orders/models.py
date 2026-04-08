from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from shop.models import Product


class Order(models.Model):
    # --- Choices ---
    DELIVERY_CHOICES = [
        (300, "Nairobi (Within 10km) - KES 300"),
        (500, "Nairobi (Outside 10km) - KES 500"),
        (700, "Outside Nairobi (G4S/Wells Fargo) - KES 700"),
    ]

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    )

    # New choices for the merchant fulfillment workflow
    SHIPPING_STATUS_CHOICES = (
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    # --- Fields ---
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", null=True, blank=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    county = models.CharField(max_length=100, default="Nairobi")
    city_estate = models.CharField(max_length=100)
    address = models.CharField(max_length=250)

    delivery_fee = models.DecimalField(
        max_digits=10, decimal_places=2, choices=DELIVERY_CHOICES, default=300
    )

    # --- Payment & Status ---
    ipay_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    # ADDED: Tracking and Shipping Status for Merchant Dashboard
    shipping_status = models.CharField(
        max_length=20, choices=SHIPPING_STATUS_CHOICES, default="processing"
    )
    tracking_number = models.CharField(max_length=100, blank=True, null=True)

    total_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_cost_with_delivery(self):
        return self.get_total_cost() + self.delivery_fee

    def update_total_paid(self):
        # Using F expression or direct assignment is better for atomic updates
        self.total_paid = self.get_total_cost()
        self.save(update_fields=["total_paid"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Item {self.id} for Order {self.order.id}"

    def get_cost(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.update_total_paid()
