#encoding: utf-8

from django.views.generic import TemplateView, ListView

from catalog.models import Product

class HomeView(ListView):

    template_name = 'home.html'
    paginate_by = 3
    
    def get_queryset(self):
        return Product.objects.filter(featured=True)