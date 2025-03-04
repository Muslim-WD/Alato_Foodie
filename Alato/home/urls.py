from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.customer_login, name="customer_login"),
    path('signup/', views.customer_signup, name="customer_signup"),
    path('logout/', views.customer_logout, name="customer_logout"),
    # path('admin_/', views.admin_login, name="admin_login"),

    path('add_to_cart/<int:food_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('order_now/', views.order_now, name='order_now'),
    path('orders/', views.order_confirmation, name='order_confirmation'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),  # New line for order details
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/add/', views.add_restaurant, name='add_restaurant'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    # path('restaurant/<int:pk>/add_food_item/', views.add_food_item, name='add_food_item'),
]
