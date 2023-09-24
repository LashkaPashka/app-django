from django.urls import path, include
from products.views import ProductsViews, basket_add, basket_remove
app_name = 'products'

urlpatterns = [
    path('', (ProductsViews.as_view()), name='index'),
    path('category/<int:category_id>/', ProductsViews.as_view(), name='category'),
    path('page/<int:page>/', ProductsViews.as_view(), name='paginator'),
    path('baskets/add/<int:product_id>', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>', basket_remove, name='basket_remove'),
]