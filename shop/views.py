from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm  # Make sure this matches your forms.py class name
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def product_list(request, category_slug=None):
    category = None
    # We get ALL categories so the template can loop through parents and children
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    featured_products = Product.objects.filter(featured=True, available=True)[:5]

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        # Logic: Show products in THIS category AND all categories underneath it
        # We use a custom method or set of IDs
        category_ids = [category.id] + [c.id for c in category.children.all()]
        # If you have 3 levels, you might need a deeper loop or the get_descendants method
        products = products.filter(category_id__in=category_ids)
    # --- Pagination Logic ---
    paginator = Paginator(products, 9)  # Show 9 products per page (3x3 grid)
    page = request.GET.get("page")

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return render(
        request,
        "shop/product/list.html",
        {
            "category": category,
            "categories": categories,
            "products": products,  # This is now a Page object, not a QuerySet
        },
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    related_products = Product.objects.filter(
        category=product.category, available=True
    ).exclude(id=product.id)[:3]

    if not related_products.exists():
        related_products = (
            Product.objects.filter(available=True)
            .exclude(id=product.id)
            .order_by("?")[:3]
        )

    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "cart_product_form": cart_product_form,
            "related_products": related_products,
        },
    )


@user_passes_test(lambda u: u.is_staff)
def product_list_admin(request):
    products = Product.objects.all().order_by("-created")
    return render(request, "shop/admin/product_list.html", {"products": products})


@user_passes_test(lambda u: u.is_staff)
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("shop:product_list_admin")
    else:
        form = ProductForm()
    return render(request, "shop/admin/product_form.html", {"form": form})
