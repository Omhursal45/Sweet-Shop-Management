from django.contrib import admin
from .models import Sweet, Cart, CartItem, Order, OrderItem


@admin.register(Sweet)
class SweetAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'quantity', 'is_available', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'category', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'created_at']
    inlines = [CartItemInline]
    readonly_fields = ['id', 'created_at', 'updated_at']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'id']
    inlines = [OrderItemInline]
    readonly_fields = ['id', 'created_at', 'updated_at']
