from django.db import models
from django.urls import reverse


class Category(models.Model):
    parent = models.ForeignKey(
        "self", related_name="children", on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return " -> ".join(full_path[::-1])


def get_descendants(self, include_self=True):
    """Helper to get all sub-categories recursively"""
    descendants = []
    if include_self:
        descendants.append(self)
    for child in self.children.all():
        descendants.extend(child.get_descendants(include_self=True))
    return descendants


class Product(models.Model):
    category = models.ForeignKey(
        "Category", related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    brand = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)

    # Pricing logic
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False, db_index=True)  # Added here!

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Health Specific Fields
    benefits = models.TextField(
        blank=True, help_text="Enter each benefit on a new line"
    )
    usage = models.TextField(
        blank=True, help_text="Dosage instructions (e.g., 1 tablet daily)"
    )
    location = models.CharField(max_length=100, default="Nairobi Warehouse")

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["id", "slug"]),
        ]

    def __str__(self):
        return self.name

    def get_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/additional/%Y/%m/%d")
    is_thumbnail = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"
