from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
# Create your tests here.
from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):
    def test_control(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')
        
    def _common_(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/products.html')


class ProductViewTestCase(TestCase):
    fixtures = ['categories.json', 'product.json']

    def test_products(self):
        path = reverse('products:index')
        response = self.client.get(path)
        self._common_test(response)

        products = Product.objects.all()
        self.assertEqual(list(response.context_data['object_list']), list(products[:3]))


    def test_categories(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)
        self._common_test(response)

        products = Product.objects.all()
        self.assertEqual(list(response.context_data['object_list']), list(products.filter(category_id=category.id)))


    def _common_test(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/products.html')