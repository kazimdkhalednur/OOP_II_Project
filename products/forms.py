from django import forms

from .models import Cart


class CartForm(forms.ModelForm):
    product_slug = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Cart
        fields = ["quantity"]
        widgets = {
            "quantity": forms.NumberInput(
                attrs={
                    "style": "max-width: 22px; text-align: center;",
                    "min": 1,
                    "max": 5,
                    "value": 1,
                }
            ),
        }
