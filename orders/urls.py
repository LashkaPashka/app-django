from django.urls import path
from orders.views import CreateOrderViews, OrdersViews, SuccessOrdersViews, ChannelViews


app_name = 'orders'

urlpatterns = [
    path('create_order/', CreateOrderViews.as_view(), name='create_order'),
    path('my-orders/', OrdersViews.as_view(), name='my-orders'),
    path('my-success/', SuccessOrdersViews.as_view(), name='my-success'),
    path('my-channel/', ChannelViews.as_view(), name='my-channel'),
]