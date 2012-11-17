#encoding: utf-8

from django.db import models

class Category(models.Model):

    name = models.CharField(verbose_name=u'Nome', max_length=100,
        help_text=u'O nome da categoria')
    slug = models.SlugField(verbose_name=u'Apelido', max_length=100)

    created_on = models.DateTimeField(auto_now_add=True, 
        verbose_name=u'Criado em')
    updated_on = models.DateTimeField(auto_now=True, 
        verbose_name=u'Atualizado em')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Categoria'
        verbose_name_plural = u'Categorias'
        ordering = ['name']

class Product(models.Model):

    name = models.CharField(verbose_name=u'Nome', max_length=100,
        help_text=u'O nome do produto')
    slug = models.SlugField(verbose_name=u'Apelido', max_length=100)
    category = models.ForeignKey(Category, verbose_name=u'Categoria',
        related_name=u'products', null=True, blank=True)
    price = models.DecimalField(verbose_name=u'Preço R$',
        max_digits=6, decimal_places=2)
    description = models.TextField(verbose_name=u'Descrição',
        blank=True)
    photo = models.ImageField(upload_to='products', verbose_name=u'Foto',
        null=True, blank=True)
    featured = models.BooleanField(verbose_name=u'Destaque?',
        default=False, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('product_details', (), {'slug': self.slug})

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Produto'
        verbose_name_plural = u'Produtos'
        ordering = ['name']