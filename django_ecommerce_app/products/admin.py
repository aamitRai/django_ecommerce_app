from django.contrib import admin

# Register your models here.
from .models import *

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    fk_name = 'product_instance'

@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    model = ColorVariant
    list_display=['color_name','price']

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    model = SizeVariant
    list_display=['size','price']
    
    

class ProductAdmin(admin.ModelAdmin):
    list_display=[ 'product_name','category_name','price']
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

admin.site.register(Coupan)