from django.contrib import admin
from .models import Category, Product, ProductImage


# This allows you to add images directly on the Product page
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Shows one empty slot for a new image by default


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Added 'parent' to list_display so you see the hierarchy
    list_display = ["name", "parent", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["parent"]

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Added 'brand' and 'discount_price' to the display
    list_display = [
        "name",
        "brand",
        "price",
        "discount_price",
        "stock",
        "available",
        "created",
    ]
    list_filter = ["available", "brand", "category", "created"]
    # Allows quick editing of prices and stock levels from the list view
    list_editable = ["price", "discount_price", "stock", "available"]
    prepopulated_fields = {"slug": ("name",)}

    # This attaches the images to the product form
    inlines = [ProductImageInline]

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image", "is_thumbnail"]
    list_filter = ["is_thumbnail"]
    list_editable = ["is_thumbnail"]
