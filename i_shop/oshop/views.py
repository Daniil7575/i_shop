from django.shortcuts import render, get_object_or_404

from .models import Category, Product
from cart.forms import CartAddProductForm


def product_list(request, cat_slug=None):
    cat = None
    cats = Category.objects.all()
    products = Product.objects.filter(available=True)
    print(cat_slug)
    if cat_slug:
        # try:
        # except Exception:
        cat = get_object_or_404(Category, slug=cat_slug)

        products = products.filter(category=cat)

    context = {
        'category': cat,
        'categories': cats,
        'products': products
    }

    return render(request, 'oshop/list.html', context)


def product_detail(requset, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(
        requset,
        'oshop/detail.html',
        {'product': product,
         'cart_product_form': cart_product_form}
    )
