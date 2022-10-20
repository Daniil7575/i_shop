from django.shortcuts import render, get_object_or_404

from .models import Category, Product

def product_list(request, cat_slug=None):
    cat = None
    cats = Category.objects.all()
    products = Product.objects.filter(available=True)
    if cat_slug:
        # try:
        # except Exception:
        cat = Category.objects.get(slug=cat_slug)
        products = products.filter(category=cat)

        context = {
            'cat': cat,
            'cats':cats,
            'products': products
        }

    return render(request, 'oshop/product/list.html', context)


def product_detail(requset, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(
        requset,
        'oshop/product/detail.html',
        {'product': product}
    )
