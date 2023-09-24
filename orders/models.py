from django.db import models
from user.models import User
# Create your models here.
from products.models import Baskets



class OrdersCreate(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.TimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order {self.id} for {self.initiator}'



    def after_payment(self):
        baskets = Baskets.objects.filter(user=self.initiator)
        self.basket_history = {
            'purchased_items': [basket.db_json() for basket in baskets],
            'total_sum': baskets.total_sum(),
        }
        baskets.delete()
        self.save()

