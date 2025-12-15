"""
Context processors for sweets app
"""
from .models import Cart


def cart_context(request):
    """Add cart information to template context"""
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {'cart': None, 'cart_count': 0}
    
    try:
        cart = Cart.objects.get(user=request.user)
        return {
            'cart': cart,
            'cart_count': cart.total_items
        }
    except Cart.DoesNotExist:
        return {'cart': None, 'cart_count': 0}
    except Exception:
        return {'cart': None, 'cart_count': 0}
