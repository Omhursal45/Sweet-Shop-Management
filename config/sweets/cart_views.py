"""
Cart and Order Views for E-commerce Functionality
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Sweet, Cart, CartItem, Order, OrderItem
from django.http import JsonResponse


def get_or_create_cart(user):
    """Get or create cart for user"""
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
    return cart


@login_required
def add_to_cart(request, id):
    """Add sweet to cart"""
    sweet = get_object_or_404(Sweet, id=id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        messages.error(request, "Quantity must be greater than 0")
        return redirect('sweet_detail', id=sweet.id)
    
    if sweet.quantity < quantity:
        messages.error(request, f"Only {sweet.quantity} items available in stock")
        return redirect('sweet_detail', id=sweet.id)
    
    cart = get_or_create_cart(request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        sweet=sweet,
        defaults={'quantity': quantity}
    )
    
    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > sweet.quantity:
            messages.error(request, f"Only {sweet.quantity} items available in stock")
            return redirect('sweet_detail', id=sweet.id)
        cart_item.quantity = new_quantity
        cart_item.save()
    
    messages.success(request, f"{sweet.name} added to cart!")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'message': f"{sweet.name} added to cart!"
        })
    
    return redirect('sweet_detail', id=sweet.id)


@login_required
def view_cart(request):
    """View shopping cart"""
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all()
    
    return render(request, 'sweets/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
    })


@login_required
def update_cart_item(request, id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, "Item removed from cart")
    elif quantity > cart_item.sweet.quantity:
        messages.error(request, f"Only {cart_item.sweet.quantity} items available in stock")
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated")
    
    return redirect('view_cart')


@login_required
def remove_from_cart(request, id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=id, cart__user=request.user)
    sweet_name = cart_item.sweet.name
    cart_item.delete()
    messages.success(request, f"{sweet_name} removed from cart")
    return redirect('view_cart')


@login_required
def clear_cart(request):
    """Clear entire cart"""
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    messages.success(request, "Cart cleared")
    return redirect('view_cart')


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem, UserAddress

@login_required
def checkout(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.select_related("sweet")

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect("view_cart")

    # Stock check
    for item in cart_items:
        if item.quantity > item.sweet.quantity:
            messages.error(
                request,
                f"{item.sweet.name} - Only {item.sweet.quantity} available"
            )
            return redirect("view_cart")

    # Load default address
    default_address = UserAddress.objects.filter(
        user=request.user,
        is_default=True
    ).first()

    if request.method == "POST":
        shipping_address = request.POST.get("shipping_address", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        payment_method = request.POST.get("payment_method", "COD")
        save_address = request.POST.get("save_address")

        if not shipping_address or not phone_number:
            messages.error(request, "Address and phone number are required")
            return render(request, "sweets/checkout.html", {
                "cart": cart,
                "cart_items": cart_items,
                "default_address": default_address
            })

        with transaction.atomic():
            # Save address if requested
            if save_address:
                UserAddress.objects.update_or_create(
                    user=request.user,
                    is_default=True,
                    defaults={
                        "address": shipping_address,
                        "phone_number": phone_number
                    }
                )

            order = Order.objects.create(
                user=request.user,
                total_amount=cart.total_price,
                shipping_address=shipping_address,
                phone_number=phone_number,
                payment_method=payment_method,
                status="pending"
            )

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    sweet=cart_item.sweet,
                    quantity=cart_item.quantity,
                    price=cart_item.sweet.price
                )

                cart_item.sweet.quantity -= cart_item.quantity
                cart_item.sweet.save(update_fields=["quantity"])

            cart.items.all().delete()

        messages.success(
            request,
            f"Order placed successfully! Order ID: {str(order.id)[:8]}"
        )
        return redirect("order_detail", id=order.id)

    return render(request, "sweets/checkout.html", {
        "cart": cart,
        "cart_items": cart_items,
        "default_address": default_address
    })



@login_required
def order_list(request):
    """View user's order history"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'sweets/orders.html', {
        'orders': orders,
    })


@login_required
def order_detail(request, id):
    """View order details"""
    order = get_object_or_404(Order, id=id, user=request.user)
    return render(request, 'sweets/order_detail.html', {
        'order': order,
    })


@login_required
def cart_count(request):
    """Get cart item count for AJAX"""
    try:
        cart = get_or_create_cart(request.user)
        count = cart.total_items
    except Exception as e:
        count = 0
    return JsonResponse({'count': count})

