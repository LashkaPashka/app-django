# Generated by Django 3.2.13 on 2023-08-17 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_baskets'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=178, null=True),
        ),
    ]
