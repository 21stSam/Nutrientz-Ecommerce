# shop/forms.py

from django import forms
from .models import Product

# Max quantity is 20 for simplicity
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    # This choice includes 0 for removing the item from the cart
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        empty_value=1,  # Default to 1 if no selection
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),  # Optional: add a class for styling
    )

    # This hidden field tracks whether the user is UPDATING the cart
    # It will be set to True on the cart page when updating quantity/removing
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    # NEW: Add a hidden field to pass the product_id easily when submitting the form
    product_id = forms.IntegerField(widget=forms.HiddenInput)


# Add this to the bottom of shop/forms.py


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Include all fields the client needs to edit
        fields = [
            "category",
            "name",
            "slug",
            "image",
            "description",
            "price",
            "available",
            "featured",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "auto-generated-if-blank",
                }
            ),
        }
