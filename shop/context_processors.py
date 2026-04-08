# shop/context_processors.py

from .cart import Cart

def cart(request):
    """
    Makes the cart object available to all templates.
    """
    return {'cart': Cart(request)}