# orders/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from products.models import Product

@receiver(post_save, sender=Order)
def update_product_stock(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        if product.stock >= instance.quantity:
            product.stock -= instance.quantity
            product.save()
        else:
            # Optional: Raise an alert or rollback if not enough stock
            print("Insufficient stock for this order.")
