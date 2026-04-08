from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """Calculate the total cost of all items in the cart."""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values())

    # cart/cart.py

    def __iter__(self):
        """
            Iterate over the items in the cart and get the products from the database.
                                    """
        product_ids = self.cart.keys()
        # Get the product objects from the database
        products = Product.objects.filter(id__in=product_ids)

        # Create a copy so we don't modify the session-stored dictionary
        cart = self.cart.copy()

        # Create a mapping for quick lookup
        product_map = {str(p.id): p for p in products}

        for product_id, item in cart.items():
            # Get the actual product object
            product = product_map.get(product_id)

            # We yield a NEW dictionary for each item.
            # This keeps the 'Product' object and 'Decimal' out of the session.
            yield {
                'product': product,
                'quantity': item['quantity'],
                'price': Decimal(item['price']),
                'total_price': Decimal(item['price']) * item['quantity']
            }


