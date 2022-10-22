from django.shortcuts import render
from django.http import HttpRequest

from .models import OrderItem
from .tasks import order_created
from .forms import OrderCreationForm
from cart.cart import Cart


def order_create(request: HttpRequest):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreationForm()
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})
