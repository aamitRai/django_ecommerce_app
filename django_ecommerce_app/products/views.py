from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import *

def get_particluar_product(request,slug):
      try:
        product = Product.objects.get(product_slug=slug)
        if request.GET.get('size'):
          size=request.GET.get('size')
          print("size",size)
          product.price=get_price_by_size(product,size)
      except Product.DoesNotExist:
        raise Http404("Product not found")
      context={'product':product}
      return  render (request,'products/single_product.html',context)
def show_products(request):
    return render(request,'products/showProducts.html')

def add_product(request):
    return render(request,'products/addProduct.html')
    
def delete_product(request):  
    return render(request,'products/showProducts.html')


def index(request):
    products=Product.objects.all()
    print("products", products)
    context={'products':products}
    return render(request,'products/index.html',context)
    
    
    #this function return product prize by size
    
def get_price_by_size(self,size):
      sizeObj=SizeVariant.objects.get(size=size)
      if sizeObj:
        return self.price+sizeObj.price
      return self.price
      
      
      