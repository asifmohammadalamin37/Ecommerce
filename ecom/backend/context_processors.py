from .models import Customer, OrderCart, UserPermission
from .views import cart_amount_summary

def menu_items(request):
    menu_list = UserPermission.objects.filter(user_id=request.user.id).values_list('menu__menu_name', flat=True)
    search_menu_list = UserPermission.objects.filter(user_id=request.user.id, menu__menu_name__icontains='search').values_list('menu__menu_name', flat=True)

    return {'main_menu_list': menu_list, 'search_menu_list': search_menu_list}

def get_cart_item(request):
    if request.user.is_authenticated:
        try:
            custormer = Customer.objects.filter(user=request.user).first()
            cart_items = OrderCart.objects.filter(customer=custormer, is_order=False, is_active=True)
        except Customer.DoesNotExist:
            cart_items = []
    else:
        cart_items = []
    
    amount_summary = cart_amount_summary(request)
    cart_item_count = cart_items.count() if hasattr(cart_items, 'count') else len(cart_items)
    return {
        'cart_items': cart_items,
        'cart_item_count': cart_item_count,
        'amount_summary': amount_summary
    }