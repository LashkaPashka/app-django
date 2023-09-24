from django.db import models
from user.models import User
import stripe
from django.conf import settings


# Create your models here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_product(self):
        line_items = []
        for basket in self:
            items = {
                'price': basket.product.stripe_product_id,
                'quantity': basket.quantity,
            }
            line_items.append(items)
        return line_items



class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    stripe_product_id = models.CharField(max_length=178, null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.PROTECT)

    def __str__(self):
        return f"Название {self.name} | Категоря {self.category.name}"


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_id:
            current = self.create_product_price()
            self.stripe_product_id = current['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)



    def create_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(product=stripe_product['id'], unit_amount=round(self.price*100), currency='rub',)
        return stripe_product_price



class Baskets(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина {self.user.username} | Продукт {self.product.name}"

    def sum(self):
        return self.quantity*self.product.price

    def db_json(self):
        basket_item = {
            'name': self.product,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item
