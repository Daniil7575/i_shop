from decimal import Decimal
from django.conf import settings
from django.http import HttpRequest
from oshop.models import Product


class Cart:
    def __init__(self, request: HttpRequest) -> None:
        """Initialize cart object"""

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['quantity'] * item['price']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self,
            product: Product,
            quantuty: int = 1,
            update_quantity: bool = False) -> None:

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if update_quantity:
            self.cart[product_id]['quantity'] = quantuty
        else:
            self.cart[product_id]['quantity'] += quantuty

    def save(self):
        self.session.modified = True

    def remove(self, product: Product) -> None:
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self) -> Decimal:
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self) -> None:
        del self.session[settings.CART_SESSION_ID]
        self.save()
