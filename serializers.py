from rest_framework import serializers
from .models import Order
from products.models import Product  # Import Product model

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')

        if product.stock < quantity:
            raise serializers.ValidationError(
                f"Only {product.stock} items left in stock for {product.pname}."
            )
        return data
