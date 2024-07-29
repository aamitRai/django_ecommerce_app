from django.shortcuts import render

def index(request):
    return  render(request,"common/index.html")

def about(request):
    return  render(request,"common/about.html")
    
    
def contact(request):
    return  render(request,"common/contact.html")
    