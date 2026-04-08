# shop/cart.py
import copy
from decimal import Decimal
from django.conf import settings
from .models import Product
from .forms import CartAddProductForm

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        
        # Ensure the CART_SESSION_ID key exists in the session dictionary.
        # This structure is the most robust for persistence.
        if settings.CART_SESSION_ID not in self.session:
            self.session[settings.CART_SESSION_ID] = {}
            
        self.cart = self.session[settings.CART_SESSION_ID]

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                # Store price as string to avoid session serialization issues
                'price': str(product.price) 
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            
        self.save()

    def save(self):
        """
        Explicitly assign the cart back to the session and mark as modified.
        This is critical for ensuring persistence across requests.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
    def __iter__(self):
        """
        Iterate over the items in the cart and fetch the products from the database.
        """
        product_ids = self.cart.keys()
        
        # Get the product objects
        products = Product.objects.filter(id__in=product_ids)
        
        # Use deep copy to avoid modifying session data
        cart = copy.deepcopy(self.cart)
        
        for product in products:
            cart[str(product.id)]['product'] = product  

        for item in cart.values():
            item['price'] = Decimal(item['price']) 
            item['total_price'] = item['price'] * item['quantity']
            item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity': item['quantity'],
                'update': True,
                'product_id': item['product'].id
            })
            yield item
            
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total cost of the items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())

    def clear(self):
        """
        Remove the cart from the session and reset the instance's cart dictionary.
        """
        try:
            del self.session[settings.CART_SESSION_ID]
        except KeyError:
            pass # Already cleared
            
        self.cart = {} # Reset the instance variable
        self.save() # Mark session modified, but with the cart key deleted (cleaner)