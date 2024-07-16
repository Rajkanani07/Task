from django.db import models

# Create your models here.

class Product_Details(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(blank=False, null=False, max_length=25, unique=True)
    category = models.CharField(blank=False, null=False, max_length=50)
    price = models.IntegerField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    SIZES = (
        ("XXL", "double extra large"),
        ("XL", "extra large"),
        ("L", "large"),
        ("M", "medium"),
        ("S", "small"),
        ("XXXl", "triple extra large"),
    )
    sizes = models.CharField(blank=False, null=False, max_length=20, choices=SIZES)
    colour = models.CharField(blank=False, null=False, max_length=20)
    fabric = models.CharField(blank=False, null=False, max_length=20)
    preferred_season = models.CharField(blank=True, null=True, max_length=20)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=True)
