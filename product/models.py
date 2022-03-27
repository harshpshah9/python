from django.db import models
from django_extensions.db.models import *


class Category(TimeStampedModel, models.Model):
    name = models.CharField(max_length=150, null=True)
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    slug = AutoSlugField(populate_from='name')

    def slugify_function(self, content):
        return content.replace('_', '-').lower()

    def __str__(self):
        return self.name

    # @property
    # def category_count(self):
    #     print(">>>>>>>>>", self.category.all())
    #     parent= Category.objects.all(parent=self)
    #     return parent

    @property
    def sub_category_count(self):
        return self.category.count()


class Brand(TimeStampedModel, models.Model):
    name = models.CharField(max_length=150, null=True)
    slug = AutoSlugField(populate_from='name')

    def slugify_function(self, content):
        return content.replace('_', '-').lower()

    def __str__(self):
        return self.name

    @property
    def brand_count(self):
        return self.brand.count()


class Product(TimeStampedModel, ActivatorModel, models.Model):
    name = models.CharField(max_length=150, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    description = models.TextField(null=False, blank=False)
    long_description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", null=True)
    brand = models.ForeignKey(Brand, related_name='brand', on_delete=models.CASCADE, null=True)
    slug = AutoSlugField(populate_from='name')

    def slugify_function(self, content):
        return content.replace('_', '-').lower()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/', null=True)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.image.url


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE)
    key = models.CharField(max_length=25)
    value = models.CharField(max_length=25)

    def __str__(self):
        return str(self.product)
