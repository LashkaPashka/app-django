from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.models import Baskets
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from products.models import Product, ProductCategory
from coom.views import TitleMixin
from django.core.cache import cache


class IndexViews(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'



class ProductsViews(TitleMixin, ListView):
    model = Product
    title = 'Store'
    template_name = 'products/products.html'
    paginate_by = 3


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsViews, self).get_context_data(**kwargs)
        categories = cache.get('categories')
        if not categories:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories'] = categories
        return context

    def get_queryset(self):
        queryset = super(ProductsViews, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = Baskets.objects.filter(user=request.user, product=product)
    if not basket.exists():
        basket.create(user=request.user, product=product, quantity=1)
    else:
        basket = basket.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Baskets.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])





'''def products(request, category_id=None, page_number=1):
    product = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    per_page = 3
    paginator = Paginator(product, per_page)
    products_paginator = paginator.page(page_number)
    context = {"title": "Store", "products": products_paginator,
    "categories": ProductCategory.objects.all()}
    return render(request, 'products/products.html', context)'''

