from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    # This creates a dropdown for 1-20 items
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    # Hidden field to tell the cart if we are adding to or replacing the total
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
