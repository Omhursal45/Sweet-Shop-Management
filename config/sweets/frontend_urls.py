from django.urls import path
from . import views 
from . import cart_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sweets/', views.sweets_list, name='sweets_list'),
    path('sweet/<uuid:id>/', views.sweet_detail, name='sweet_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('purchase/<uuid:id>/', views.purchase_sweet, name='purchase_sweet'),
    path('sweet/<uuid:id>/edit/', views.update_sweet, name='update_sweet'),
    path('sweet/<uuid:id>/delete/', views.delete_sweet, name='delete_sweet'),
    path('sweet/add/', views.add_sweet, name='add_sweet'),
    
    # Cart URLs
    path('cart/', cart_views.view_cart, name='view_cart'),
    path('cart/add/<uuid:id>/', cart_views.add_to_cart, name='add_to_cart'),
    path('cart/update/<uuid:id>/', cart_views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<uuid:id>/', cart_views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', cart_views.clear_cart, name='clear_cart'),
    path('cart/count/', cart_views.cart_count, name='cart_count'),
    
    # Order URLs
    path('checkout/', cart_views.checkout, name='checkout'),
    path('orders/', cart_views.order_list, name='order_list'),
    path('order/<uuid:id>/', cart_views.order_detail, name='order_detail'),
]
