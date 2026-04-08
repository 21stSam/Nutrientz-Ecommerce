from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "county",
            "city_estate",
            "address",
            "delivery_fee",
        ]

        widgets = {
            "delivery_fee": forms.Select(attrs={"class": "form-select"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email Address", "class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "0712 345 678", "class": "form-control"}),
            "county": forms.TextInput(attrs={"placeholder": "e.g. Nairobi", "class": "form-control"}),
            "city_estate": forms.TextInput(attrs={"placeholder": "e.g. Kilimani", "class": "form-control"}),
            "address": forms.Textarea(attrs={
                "placeholder": "Apartment/House Number",
                "class": "form-control",
                "rows": 3,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_fee'].label = "Select Delivery Area"