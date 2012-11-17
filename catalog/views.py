#encoding: utf-8

from django.views.generic import DetailView, ListView

from .models import Product

class ProductView(DetailView):

    template_name = 'catalog/product.html'
    model = Product
    context_object_name = 'product'

class ProductsListView(ListView):

    template_name = 'catalog/products.html'
    model = Product