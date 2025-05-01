from django.db import models
from customer.models import Customer
from product.models import Product
from django.core.validators import MinValueValidator

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer.full_name}"
    
    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())
    
    class Meta:
        ordering = ['-date']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    qty = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.qty} x {self.product.name}"
    
    @property
    def subtotal(self):
        return self.qty * self.unit_price
    
    def save(self, *args, **kwargs):
        # Store the current price when creating the order item
        if not self.unit_price:
            self.unit_price = self.product.cost
        super().save(*args, **kwargs)