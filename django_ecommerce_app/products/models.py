from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

class Category(BaseModel):
     category_name=models.CharField(max_length=100,default="unknown")
     category_slug=models.SlugField(unique=True,null=True,blank=True)
     category_image=models.ImageField(upload_to="categories")
     def __str__(self):
        return self.category_name
   
     #save method override
     def save(self,  *args , **kwargs):
          self. category_slug=slugify(self.category_name)
          super(Category, self).save(*args, **kwargs)


class ColorVariant(BaseModel):
     color_name=models.CharField(max_length=50,default="unknown")
     price=models.IntegerField(default=0)
     
     def __str__(self) :
          return self.color_name

     

class SizeVariant(BaseModel):
     size=models.CharField(max_length=50,default="unknown")
     price=models.IntegerField(default=0)
     
     def __str__(self) :
          return self.size


class Product(BaseModel):
     product_name=models.CharField( max_length=50,default='unknown')
     product_slug=models.SlugField(unique=True,null=True,blank=True)
     category_name=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
     price =models.FloatField(default=True)
     description=models.TextField()
     color_variant=models.ManyToManyField(ColorVariant)
     size_variant=models.ManyToManyField(SizeVariant)
     
          #save method override
     def save(self,  *args , **kwargs):
          self.product_slug=slugify(self.product_name)
          super(Product, self).save(*args, **kwargs)

     def __str__(self):
        return self.product_name


class ProductImage(BaseModel):
    product_instance = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_different_images")
    product_image = models.ImageField(upload_to="products")

    def __str__(self):
        return f"Image of {self.product_instance.product_name}"


class Coupan(BaseModel):
     coupan_code=models.CharField(max_length=6)
     is_expire=models.BooleanField(default=False)
     expiry_date=models.DateField()
     discount_percent=models.IntegerField(default=5) 
     minimum_amount=models.IntegerField(default=100)