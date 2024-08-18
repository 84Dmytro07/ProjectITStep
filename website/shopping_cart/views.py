from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('shopping_cart:cart_detail')  # Перенаправление на страницу корзины


def cart_detail(request):
    cart = Cart(request)
    cart_items = []
    for item in cart:
        # Проверяем, является ли item словарем или объектом
        product = item['product'] if isinstance(item, dict) else item.product
        quantity = item['quantity'] if isinstance(item, dict) else item.quantity
        total_price = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })
    return render(request, 'shopping_cart/detail.html', {'cart_items': cart_items, 'cart': cart})


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shopping_cart:cart_detail')  # Перенаправление на страницу корзины

def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity > 0:
                        product = Product.objects.get(id=product_id)
                        cart.add(product, quantity=quantity, update_quantity=True)
                except Product.DoesNotExist:
                    continue

    return redirect('shopping_cart:cart_detail')  # Перенаправление на страницу корзины





