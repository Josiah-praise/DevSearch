from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class CustomUserChangeForm(UserChangeForm):
    class meta:
        model = get_user_model()
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    class meta:
        model = get_user_model()
        fields = '__all__'
