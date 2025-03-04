from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Restaurant, FoodItem, CartItem, Order,OrderItem
from .forms import FoodItemForm, CreateUserForm, RestaurantForm, OrderForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta


def index(request):
    return render(request, 'index.html')


def customer_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, "login.html")


def customer_signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully ' + user)
            return redirect("customer_login")
    context = {'form': form}
    return render(request, 'signup.html', context=context)


    

@login_required(login_url='customer_login')
def customer_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('index')





@login_required(login_url='customer_login')
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant_list.html', {'restaurants': restaurants})


@login_required(login_url='customer_login')
def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')
    else:
        form = RestaurantForm()
    return render(request, 'add_restaurant.html', {'form': form})


@login_required(login_url='customer_login')
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    food_items = restaurant.food_items.all()
    return render(request, 'restaurant_detail.html', {'restaurant': restaurant, 'food_items': food_items})


@login_required(login_url='customer_login')
def add_food_item(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.restaurant = restaurant
            food_item.save()
            return redirect('restaurant_detail', pk=pk)
    else:
        form = FoodItemForm()
    return render(request, 'add_food_item.html', {'form': form, 'restaurant': restaurant})


@login_required(login_url='customer_login')
def add_to_cart(request, food_item_id):
    food_item = get_object_or_404(FoodItem, id=food_item_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, food_item=food_item)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required(login_url='customer_login')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = cart_items.aggregate(total=Sum(F('quantity') * F('food_item__price')))['total'] or 0

    if request.method == "POST":
        action = request.POST.get('action')
        item_id = request.POST.get('item_id')
        cart_item = CartItem.objects.get(id=item_id, user=request.user)

        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        elif action == 'remove':
            cart_item.delete()
        return redirect('cart')  # Refresh the cart page after any action

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)




@login_required(login_url='customer_login')
def order_now(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            # Calculate total price from cart items
            cart_items = CartItem.objects.filter(user=request.user)
            total_price = cart_items.aggregate(total=Sum(F('quantity') * F('food_item__price')))['total'] or 0
            order.total_price = total_price  # Assign calculated total_price

            # Set arrival time or use your own logic
            order.arrival_time = timezone.now() + timedelta(hours=1)
            order.save()

            # Create OrderItem instances for each CartItem
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    food_item=cart_item.food_item,
                    quantity=cart_item.quantity,
                    price=cart_item.food_item.price  # Copy the price
                )

            # Optionally, delete cart items after ordering
            cart_items.delete()
            messages.success(request, "Order placed successfully!")
           

            return redirect('order_confirmation')
    else:
        form = OrderForm()

    return render(request, 'order_now.html', {'form': form})






@login_required(login_url='customer_login')
def order_confirmation(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-id')
        return render(request, 'order_confirmation.html', {'orders': orders})
    else:
        return redirect('customer_login')


# views.py
@login_required(login_url='customer_login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.order_items.all()  # Retrieve OrderItem instances associated with the order
    return render(request, 'order_detail.html', {'order': order, 'items': items})




