from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from home.models import Restaurant, FoodItem, Order 
from .forms import RestaurantForm, FoodItemForm, OrderStatusForm 
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


def admin_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(f"Authenticated User: {user}") 
            if user is not None:
                login(request, user)
                if user.is_staff:  # Additional check
                    return redirect('admin_manager:manage_orders')
                else:
                    messages.error(request, 'You do not have permission to access this area.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'admin_login.html', {'form': form})


def admin_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('index')

# @login_required
def dashboard(request):
    return render(request,'admin_dashboard.html')


def admin_add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_manager:admin_restaurant_list')
    else:
        form = RestaurantForm()
    return render(request, 'add_restaurant.html', {'form': form})


def admin_restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'admin_res_list.html', {'restaurants': restaurants})


def admin_add_food_item(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.restaurant = restaurant
            food_item.save()
            return redirect('admin_manager:admin_restaurant_detail', pk=pk)
    else:
        form = FoodItemForm()
    return render(request, 'add_food_item.html', {'form': form, 'restaurant': restaurant})



def manage_orders(request):
    orders = Order.objects.all()
    if request.method == 'POST':
        form = OrderStatusForm(request.POST)
        if form.is_valid():
            order = form.cleaned_data['order']
            status = form.cleaned_data['status']
            order.status = status
            order.save()
            return redirect('admin_manager:manage_orders')
    else:
        form = OrderStatusForm()
    return render(request, 'manage_orders.html', {'orders': orders, 'form': form})


def admin_restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    food_items = restaurant.food_items.all()
    return render(request, 'admin_restaurant_detail.html', {'restaurant': restaurant, 'food_items': food_items})