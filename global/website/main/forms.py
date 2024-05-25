from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


from django import forms
from .models import Address

class OrderForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_address', 'entrance', 'door_code', 'floor', 'apartment', 'comments']
