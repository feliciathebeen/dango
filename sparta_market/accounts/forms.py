from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.urls import reverse


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ()


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "first_name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']