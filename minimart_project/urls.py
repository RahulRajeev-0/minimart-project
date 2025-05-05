from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render





urlpatterns = [
     path('', lambda request: render(request, 'home.html'), name='home'), 
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),
]