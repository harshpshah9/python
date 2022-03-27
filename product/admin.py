from django.contrib import admin

from product.models import Brand, Category, Product, ProductImage,ProductSpecification

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductSpecification)