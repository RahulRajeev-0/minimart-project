from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    in_stock = models.IntegerField()