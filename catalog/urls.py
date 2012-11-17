#encoding: utf-8

from django.conf.urls import patterns, include, url

from .views import ProductView

urlpatterns = patterns('',
    url(r'^produtos/(?P<slug>[\w_-]+)/', ProductView.as_view(),
        name='product_details'),
)
