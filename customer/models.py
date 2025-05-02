"""
Models for Customer (user)

models:
-customer 

need to consider or explore:
- authentication system 
- weather to use customer as user or not (based on app requirement)
- if got time, try to do jwt after main implementation
"""

from django.db import models

from django.core.validators import EmailValidator


# Create your models here.
from django.db import models

class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, validators=[EmailValidator()], unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        ordering = ['-created_at']