from typing import Dict
from django.http import HttpRequest

from .cart import Cart


def cart(request: HttpRequest) -> Dict[str, Cart]:
    return {'cart': Cart(request)}
