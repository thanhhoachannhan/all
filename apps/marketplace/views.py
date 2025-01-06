
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods

from .permissions import (
    marketplace_buyer_required,
)
from .models import (
    Product,
)


@marketplace_buyer_required
@require_http_methods(["GET"])
def customer_product_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'customer_product_list.html', context)

def add_to_card(request, product_id):
    return HttpResponse('add_to_card')

def customer_cart_list (request):
    return HttpResponse('customer_cart_list')

def customer_order_list (request):
    return HttpResponse('customer_order_list')
