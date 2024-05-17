from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "phone_number",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
