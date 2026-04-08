from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm  # We'll need this for quantity
from django.http import JsonResponse
from django.template.loader import render_to_string  # Add this import


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        quantity = form.cleaned_data["quantity"]
        override = form.cleaned_data["override"]
    else:
        quantity = 1
        override = False

    cart.add(product=product, quantity=quantity, override_quantity=override)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # Render ONLY the inside of the cart sidebar
        html = render_to_string(
            "cart/sidebar_content.html", {"cart": cart}, request=request
        )
        return JsonResponse(
            {
                "status": "success",
                "cart_len": len(cart),
                "sidebar_html": html,  # Send the fresh HTML back!
            }
        )

    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    # We add this so users can update quantities directly in the cart
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True}
        )
    return render(request, "cart/detail.html", {"cart": cart})


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")
