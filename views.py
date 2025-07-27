from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from cart.models import Cart
from orders.models import Order
from users.models import UserData
from products.models import Product
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

#View All Orders (Admin Only)
@api_view(['GET'])
def getAllOrders(request, username):  # take from path
    try:
        user = UserData.objects.get(username=username)
        if user.usertype != 'admin':
            return Response({"error": "Only admin can view all orders"}, status=403)

        orders = Order.objects.all().values()
        return Response(orders)
    except UserData.DoesNotExist:
        return Response({"error": "Invalid user"}, status=400)


# 1. Create Order API
@api_view(['POST'])
def createOrder(request):
    data = request.data
    try:
        user = UserData.objects.get(username=data['username'])
        product = Product.objects.get(pname=data['pname'])
        quantity = int(data['quantity'])
        total_price = quantity * product.price

        order = Order.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            total_price=total_price,
            status='Pending'
        )
        return Response({"message": "Order placed successfully", "order_id": order.id})
    except UserData.DoesNotExist:
        return Response({"error": "Invalid user"}, status=400)
    except Product.DoesNotExist:
        return Response({"error": "Invalid product"}, status=400)

#View Orders by User
@api_view(['GET'])
def getUserOrders(request):
    username = request.GET.get('username')
    try:
        user = UserData.objects.get(username=username)
        orders = Order.objects.filter(user=user).values()
        return Response(list(orders))
    except UserData.DoesNotExist:
        return Response({"error": "User not found"}, status=400)

#Update Order Status (Admin Only)
@api_view(['PUT'])
def updateOrderStatus(request):
    data = request.data
    try:
        admin = UserData.objects.get(username=data['username'])
        if admin.usertype != 'admin':
            return Response({"error": "Only admin can update order status"}, status=403)

        order = Order.objects.get(id=data['order_id'])
        order.status = data['status']
        order.save()
        return Response({"message": "Order status updated successfully"})
    except UserData.DoesNotExist:
        return Response({"error": "Invalid admin"}, status=400)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

#Cancel Order (User)
@api_view(['PUT'])
def cancelOrder(request):
    data = request.data
    try:
        user = UserData.objects.get(username=data['username'])
        order = Order.objects.get(id=data['order_id'], user=user)
        if order.status != 'Pending':
            return Response({"error": "Only pending orders can be cancelled"}, status=403)
        order.status = 'Cancelled'
        order.save()
        return Response({"message": "Order cancelled successfully"})
    except UserData.DoesNotExist:
        return Response({"error": "Invalid user"}, status=400)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def checkout_carts(request):
    user = request.user  # Authenticated user

    try:
        cart = Cart.objects.get(user=user)
        items = cart.items.select_related('product').all()

        if not items:
            return Response({'message': 'Cart is empty'}, status=400)

        total_amount = 0
        for item in items:
            total_price = item.quantity * item.product.price
            Order.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity,
                total_price=total_price,
            )
            total_amount += total_price

        items.delete()  # Clear cart after order
        return Response({'message': 'Checkout successful', 'total': total_amount})

    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=404)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).values()
    return Response(list(orders))

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_orders(request):
    user = request.user
    if user.usertype != 'admin':
        return Response({"error": "Only admin can view all orders"}, status=403)

    orders = Order.objects.all().values()
    return Response(list(orders))

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_order_status(request):
    user = request.user
    if user.usertype != 'admin':
        return Response({"error": "Only admin can update status"}, status=403)

    order_id = request.data.get('order_id')
    status_value = request.data.get('status')

    try:
        order = Order.objects.get(id=order_id)
        order.status = status_value
        order.save()
        return Response({"message": "Order status updated"})
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cancel_order(request):
    user = request.user
    order_id = request.data.get('order_id')

    try:
        order = Order.objects.get(id=order_id, user=user)
        if order.status != 'Pending':
            return Response({"error": "Only pending orders can be cancelled"}, status=403)
        order.status = 'Cancelled'
        order.save()
        return Response({"message": "Order cancelled successfully"})
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)
