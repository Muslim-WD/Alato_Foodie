from django import forms
from .models import Restaurant,FoodItem,Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class CreateUserForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=10,
        min_length=10,
        required=True,
        label="Phone Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
        help_text="Phone number must start with 6, 7, 8, or 9."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    # Custom validation for the phone number
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not re.match(r'^[6-9]\d{9}$', phone):
            raise forms.ValidationError("Phone number must start with 6, 7, 8, or 9 and be 10 digits long.")
        return phone


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'cuisine', 'rating', 'image']



class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'price', 'image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone_number']