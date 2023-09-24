from django.contrib import admin

# Register your models here.

from products.models import ProductCategory
from products.models import Product, Baskets

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Baskets)