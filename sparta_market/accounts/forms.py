from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.urls import reverse
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'image']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "image",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get("password"):
            password_help_text = (
                "You can change the password " '<a href="{}">here</a>.'
            ).format(f"{reverse('accounts:change_password')}")
            self.fields["password"].help_text = password_help_text
