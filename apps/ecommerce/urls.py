from django.urls import path, include

from ecommerce.views import (
    index,
    NotificationView,
    ForbiddenView,
    ProductView,
    OrderView,

    CustomerProductListView, CustomerProductDetailView,
    CustomerOrderListView, CustomerOrderDetailView,
    CustomerCartListView,

    customer_product_list,
)

app_name = 'ecommerce'

urlpatterns = [
    path('', index, name='index'),
    path('403', ForbiddenView.as_view(), name='403'),
    path('notification_list/', NotificationView.as_view(), name='notification_list'),
    path('product_list/', ProductView.as_view(), name='product_list'),
    path('order_list/', OrderView.as_view(), name='order_list'),

    path('customer/', include([
        path('', index),
        path('product/', include([
            path('', customer_product_list, name='customer_product_list'),
            path('detail/<int:product_id>/', CustomerProductDetailView.as_view(), name='customer_product_detail'),
            path('category/<str:category_slug>/', index),
        ])),
        path('cart/', include([
            path('', CustomerCartListView.as_view(), name='customer_cart_list'),
            path('add/<int:product_id>/', index),
            path('remove/<int:product_id>/', index),
            path('update/<int:product_id>/', index),
        ])),
        path('checkout/', include([
            path('', index),
            path('success/', index),
        ])),
        path('order/', include([
            path('', CustomerOrderListView.as_view(), name='customer_order_list'),
            path('detail/<int:order_id>/', CustomerOrderDetailView.as_view(), name='customer_order_detail'),
        ])),
        path('wishlist/', include([
            path('', index),
            path('add/<int:product_id>/', index),
            path('remove/<int:product_id>/', index),
        ])),
        path('profile/', include([
            path('', index),
            path('edit/', index),
            path('addresses/', include([
                path('', index),
                path('add/', index),
                path('<int:address_id>/edit/', index),
                path('<int:address_id>/delete/', index),
            ])),
        ])),
        path('auth/', include([
            path('login/', index),
            path('logout/', index),
            path('register/', index),
            path('forgot-password/', index),
            path('reset-password/<str:token>/', index),
        ])),
        path('reviews/', include([
            path('<int:product_id>/', index),
            path('<int:product_id>/add/', index),
        ])),
        path('support/', include([
            path('', index),
            path('new/', index),
            path('<int:ticket_id>/', index),
        ])),
    ])),

    path('vendor/', include([
        path('', index), # dashboard
        path('products/', include([
            path('', index),
        ])),
        path('orders/', include([
            path('', index),
        ])),
        path('inventory/', index),
        path('shipping/', include([
            path('', index),
            path('settings/', index),
        ])),
        path('payments/', include([
            path('', index),
            path('history/', index),
            path('settings/', index),
        ])),
        path('reviews/', index),
        path('discounts/', index),
        path('profile/', index),
        path('analytics/', index),
        path('support/', index),
    ])),
]
