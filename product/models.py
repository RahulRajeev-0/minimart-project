from django.db import models
from django.utils import timezone
# validation
from django.core.validators import MinValueValidator, MaxValueValidator

from decimal import Decimal

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    in_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # category
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # discount 
    discount_percentage = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0.0
    )
    discount_start = models.DateTimeField(null=True, blank=True)
    discount_end = models.DateTimeField(null=True, blank=True)
    # soft delete
    is_active = models.BooleanField(default=True)

    # need to add image field (if i got time)
     
    def __str__(self):
        return self.name
    
    # for checking if discount is active or not for product 
    @property 
    def is_discount_active(self):
        now = timezone.now()
        return (
            self.discount_percentage > 0 and
            self.discount_start and self.discount_end and
            self.discount_start <= now <= self.discount_end
        )
    
    # calculate discount price
    @property
    def discounted_price(self):
        if self.discount_percentage:
            discount_factor = Decimal(1) - (Decimal(self.discount_percentage) / Decimal(100))
            return round(self.cost * discount_factor, 2)
        return self.cost
    

    class Meta:
        ordering = ['name']


