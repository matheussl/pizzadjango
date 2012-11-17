#encoding: utf-8

from django.contrib import admin

from .models import Product, Category

admin.site.register([Product, Category])