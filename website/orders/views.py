from .models import OrderItem
from django.shortcuts import render
from .forms import OrderCreateForm
from shopping_cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # Если в будущем вы хотите сохранять информацию о пользователе
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/created.html', {'order': order})
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'address': request.user.profile.address,
            'postal_zip': request.user.profile.postal_zip,
            'country': request.user.profile.country,
            'state_country': request.user.profile.state_country,
            'phone': request.user.profile.phone,
        }
        form = OrderCreateForm(initial=initial_data)

    return render(request, 'orders/create.html', {'cart': cart, 'form': form})