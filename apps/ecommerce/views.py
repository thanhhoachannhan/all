from functools import wraps

from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.template import Context, Template
from django.views import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods

from ecommerce.models import (
    Product, Order, Cart, CartItem
)


class SuperuserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('authentication:login'))

        if not hasattr(request.user, 'ecommerceuser'):
            return redirect(reverse('403'))

        user = request.user.ecommerceuser
        if not user.is_authenticated or not hasattr(user, 'is_superuser') or not user.is_superuser:
            return redirect(reverse('403'))
        return super().dispatch(request, *args, **kwargs)

class SellerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('authentication:login'))

        if not hasattr(request.user, 'ecommerceuser'):
            return redirect(reverse('403'))

        user = request.user.ecommerceuser
        if not user.is_authenticated or not hasattr(user, 'is_seller') or not user.is_seller:
            return redirect(reverse('403'))
        return super().dispatch(request, *args, **kwargs)

class BuyerRequiredMixin():
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('authentication:login'))

        if not hasattr(request.user, 'ecommerceuser'):
            return redirect(reverse('403'))

        user = request.user.ecommerceuser
        if not user.is_authenticated or not hasattr(user, 'is_buyer') or not user.is_buyer:
            return redirect(reverse('403'))
        
        order_id = kwargs.get('order_id')
        if kwargs.get('order_id'):
            order = get_object_or_404(Order, id=order_id)
            if order.buyer != request.user.ecommerceuser:
                return HttpResponseForbidden("You can only view your own orders.")

        return super().dispatch(request, *args, **kwargs)

def htmx_render(request, template, base_template=None, context={}):
    if request.htmx or not base_template: return render(request, template, context)
    template = Template(f"""{{% extends "{base_template}" %}}\n{{% block content %}}\n\t{{% include "{template}" %}}\n{{% endblock content %}}""")
    return HttpResponse(template.render(Context(context)))

def index(request): return render(request, 'ecommerce_base.html')
def notification_list(request): return htmx_render(request, 'notification_list.html', 'ecommerce_base.html')
def product_list(request): return htmx_render(request, 'product_list.html', 'ecommerce_base.html')

class NotificationView(SellerRequiredMixin, View):
    def get(self, request):
        return htmx_render(request, 'notification_list.html', 'ecommerce_base.html')
    
class ForbiddenView(View):
    def get(self, request):
        return render(request, '403.html')
    
class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        return htmx_render(request, 'product_list.html', 'ecommerce_base.html', {
            'products': products,
        })

class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(buyer=request.user)
        return htmx_render(request, 'order_list.html', 'ecommerce_base.html', {
            'orders': orders,
        })
    
# === Dev

class CustomerProductListView(BuyerRequiredMixin, View):
    def get(self, request):
        return render(request, 'customer/product/list.html', {
            'products': Product.objects.all(), 
        })

class CustomerProductDetailView(BuyerRequiredMixin, View):
    def get(self, request, product_id):
        return render(request, 'customer/product/detail.html', {
            'product': get_object_or_404(Product, id=product_id),
        })

class CustomerCartListView(BuyerRequiredMixin, View):
    def get(self, request):
        return render(request, 'customer/cart/list.html', {
            'carts': Cart.objects.filter(buyer=request.user.ecommerceuser), 
        })
    
class CustomerOrderListView(BuyerRequiredMixin, View):
    def get(self, request):
        return render(request, 'customer/order/list.html', {
            'orders': Order.objects.filter(buyer=request.user.ecommerceuser), 
        })

class CustomerOrderDetailView(BuyerRequiredMixin, View):
    def get(self, request, order_id):
        return render(request, 'customer/order/detail.html', {
            'order': get_object_or_404(Order, id=order_id),
        })

# Customer bussiness
class AddToCartView(BuyerRequiredMixin, View):
    def post(self, request, product_id, quantity):
        pass

# Vendor

class VendorProductListView(SellerRequiredMixin, View):
    def get(self, request):
        return render(request, 'vendor/product/list.html', {
            'products': Product.objects.all(), 
        })

class VendorProductDetailView(SellerRequiredMixin, View):
    def get(self, request, product_id):
        return render(request, 'vendor/product/detail.html', {
            'product': get_object_or_404(Product, id=product_id),
        })



#### Version function base view
def seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('authentication:login'))

        if not hasattr(request.user, 'ecommerceuser'):
            return redirect(reverse('403'))

        user = request.user.ecommerceuser
        if not user.is_authenticated or not hasattr(user, 'is_seller') or not user.is_seller:
            return redirect(reverse('403'))

        return view_func(request, *args, **kwargs)

    return _wrapped_view

@seller_required
@require_http_methods(["GET"])
def customer_product_list(request):
    return render(request, 'customer/product/list.html', {
        'products': Product.objects.all(), 
    })