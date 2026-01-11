from django.shortcuts import render
from store.models import Product

def home(request):
    products = Product.objects.filter(is_active=True).select_related('category').order_by('-created_at')[:4]
    return render(request, 'core/home.html', {'products': products})

def about(request):
    return render(request, 'core/about.html')
