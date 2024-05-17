from django import forms

from accounts.models import Information

from .models import Order


class OrderForm(forms.ModelForm):
    save_address = forms.BooleanField(required=False)

    class Meta:
        model = Order
        fields = ["address", "address_2", "postal_code", "district", "save_address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["save_address"].widget.attrs.update({"class": "form-check-input"})

    def save(self, **kwargs):
        user = kwargs["user"]
        if self.cleaned_data["save_address"]:
            del self.cleaned_data["save_address"]
            information, created = Information.objects.update_or_create(
                user=user, defaults=self.cleaned_data
            )
            order = Order.objects.create(user=user, info=information)
        else:
            del self.cleaned_data["save_address"]
            order = Order.objects.create(user=user, **self.cleaned_data)

        return order
