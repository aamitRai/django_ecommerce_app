from django.urls import path
from .views import *
urlpatterns = [
    path("showproducts/", show_products)   ,
    path("addproducts/",add_product)   ,
    path("deleteproducts/", delete_product) ,  
    path("home/",index),
    path('<slug:slug>/',get_particluar_product,name='product_detail'),
    
]
