
from django.urls import path, include
from django.shortcuts import HttpResponse

from .views import *


app_name = 'marketplace'

urlpatterns = [
    path('', lambda request: HttpResponse('MKP')),
    path('customer/', include([
        path('product/', include([
            path('', customer_product_list, name='customer_product_list'),
        ])),
        path('cart/', include([
            path('', customer_cart_list, name='customer_cart_list'),
            path('add_to_card/<int:product_id>', add_to_card, name='add_to_card'),
        ])),
        path('order/', include([
            path('', customer_order_list, name='customer_order_list'),
        ])),
    ])),
]
