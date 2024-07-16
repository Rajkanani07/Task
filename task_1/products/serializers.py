from rest_framework import serializers
from .models import Product_Details


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Details
        fields = [
            "product_name",
            "category",
            "price",
            "description",
            "category",
            "sizes",
            "colour",
            "fabric",
            "description",
            "preferred_season",
        ]

    # def validate_price(self, value):
    #     if value < 0:
    #         raise serializers.ValidationError("Price must be a positive number.")
    #     return value

    # def validate_product_name(self, value):
    #     if Product_Details.objects.filter(product_name=value).exists():
    #         raise serializers.ValidationError("Product name must be unique.")
    #     return value