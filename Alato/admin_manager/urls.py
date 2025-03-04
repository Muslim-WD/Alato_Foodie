from django.urls import path
from .import views

app_name = 'admin_manager'

urlpatterns = [
    
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('add-restaurant/', add_restaurant, name='add_restaurant'),
    path('admin_restaurant/<int:pk>/add_food_item/', views.admin_add_food_item, name='admin_add_food_item'),
    path('manage-orders/', views.manage_orders, name='manage_orders'),
    path('admin_restaurants/', views.admin_restaurant_list, name='admin_restaurant_list'),
    path('admin_restaurants/add/', views.admin_add_restaurant, name='admin_add_restaurant'),
    path('admin_restaurant/<int:pk>/', views.admin_restaurant_detail, name='admin_restaurant_detail'),
]
