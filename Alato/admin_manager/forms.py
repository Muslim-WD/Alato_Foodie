from django import forms
from home.models import Restaurant, FoodItem, Order  # Adjust this import based on your app name

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'cuisine', 'rating', 'image']

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['restaurant', 'name', 'description', 'price', 'image']

class OrderStatusForm(forms.Form):
    order = forms.ModelChoiceField(queryset=Order.objects.all())
    status = forms.ChoiceField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
