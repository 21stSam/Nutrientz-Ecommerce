import hashlib
import hmac
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect("shop:product_list")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            # --- iPay Logic ---
            vendor_id = "demo"
            secret_key = "demo_key"

            # Parameters
            live, mm, mb, mpesa, telkom, curr = "0", "1", "1", "1", "1", "KES"
            cst, cl = "1", "0"

            # 1. Clean Amount (Must be a string integer for KES)
            amount = str(
                int(order.get_total_cost_with_delivery().quantize(Decimal("1")))
            )

            # 2. Secure Callback URL
            # build_absolute_uri is used to ensure iPay can find your server
            cbk = request.build_absolute_uri("/orders/callback/").strip()

            # 3. Parameters
            p1, p2 = str(order.id), f"Order_{order.id}"
            p3, p4 = "", ""

            # 4. THE iPay V3 KE HASH PATTERN (Strict Order)
            data_string = f"{live}{mm}{mb}{mpesa}{telkom}{vendor_id}{curr}{p1}{p2}{p3}{p4}{amount}{cbk}{cst}{cl}"

            # DEBUG: Uncomment the line below to check your terminal if it fails again
            # print(f"DEBUG HASH STRING: {data_string}")

            hash_key = hmac.new(
                secret_key.encode("utf-8"), data_string.encode("utf-8"), hashlib.sha256
            ).hexdigest()

            return render(
                request,
                "orders/order/payment_redirect.html",
                {
                    "order": order,
                    "vendor_id": vendor_id,
                    "hash": hash_key,
                    "amount": amount,
                    "cbk": cbk,
                    "curr": curr,
                    "p1": p1,
                    "p2": p2,
                    "p3": p3,
                    "p4": p4,
                    "live": live,
                    "mm": mm,
                    "mb": mb,
                    "mpesa": mpesa,
                    "telkom": telkom,
                    "cst": cst,
                    "cl": cl,
                },
            )
    else:
        # Initial form with user data if logged in
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            }
        form = OrderCreateForm(initial=initial_data)

    return render(request, "orders/order/create.html", {"cart": cart, "form": form})


@csrf_exempt
def payment_callback(request):
    status = request.GET.get("status")
    order_id = request.GET.get("p1")
    transaction_code = request.GET.get("txncd")  # This is the iPay/M-Pesa reference

    order = get_object_or_404(Order, id=order_id)

    # iPay success code is "aeiou"
    if status == "aeiou":
        order.status = "paid"  # Update your status choice
        order.paid = True
        order.ipay_transaction_id = transaction_code  # Fixed field name
        order.save()

        # Clear cart
        cart = Cart(request)
        cart.clear()

        return render(request, "orders/order/created.html", {"order": order})


def order_retry_payment(request, order_id):
    """
    Allows a user to retry a payment for an existing pending order.
    """
    order = get_object_or_404(Order, id=order_id, status="pending")

    # We use the same redirect logic we built for the initial checkout
    return render(
        request,
        "orders/order/redirect.html",
        {
            "order": order,
            "vendor_id": "your_vendor_id",  # Replace with your actual iPay VID
            "amount": order.get_total_cost_with_delivery(),
            # ... include other iPay hash variables here as needed ...
        },
    )


@login_required
def user_order_history(request):
    # Only logged-in customers see their own data
    return render(request, 'orders/customer/history.html')


@user_passes_test(lambda u: u.is_staff)
def merchant_dashboard(request):
    total_orders = Order.objects.count()
    # 'pending_shipping' represents orders that are PAID but haven't been dealt with yet
    pending_shipping = Order.objects.filter(status="paid").count()
    recent_orders = Order.objects.all().order_by("-created")[:10]

    context = {
        "total_orders": total_orders,
        "pending_shipping": pending_shipping,
        "recent_orders": recent_orders,
    }
    return render(request, "orders/merchant/dashboard.html", context)


@staff_member_required
def merchant_dashboard(request):
    # Only you and staff can see this!
    return render(request, "orders/merchant/dashboard.html")
