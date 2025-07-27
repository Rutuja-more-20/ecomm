from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer
from users.models import UserData  # Assuming user model is in userapp

# Get all products
@api_view(['GET'])
def getAllProducts(request):
    products = Product.objects.all().values()
    return Response(list(products))

# Get product by name
@api_view(['GET'])
def getProduct(request, pname):
    try:
        product = Product.objects.get(pname=pname)
        data = {
            'pname': product.pname,
            'price': product.price,
            'description': product.description,
            'stock': product.stock,
            'img_url': product.img_url
        }
        return Response(data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

# Add a new product (admin only)
@api_view(['POST'])
def addProduct(request):
    username = request.data.get('username')
    try:
        user = UserData.objects.get(username=username)
        if user.usertype != 'admin':
            return Response({'error': 'Only admin can add products'}, status=403)
    except UserData.DoesNotExist:
        return Response({'error': 'Invalid user'}, status=400)

    pname = request.data.get('pname')
    if Product.objects.filter(pname=pname).exists():
        return Response({'error': 'Product name already exists'})

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Product added successfully'})
    return Response(serializer.errors)

# Update product (admin only)
@api_view(['PUT'])
def updateProduct(request):
    username = request.data.get('username')
    try:
        user = UserData.objects.get(username=username)
        if user.usertype != 'admin':
            return Response({'error': 'Only admin can update products'}, status=403)
    except UserData.DoesNotExist:
        return Response({'error': 'Invalid user'}, status=400)

    pname = request.data.get("pname")
    try:
        product = Product.objects.get(pname=pname)
        product.price = request.data.get("price", product.price)
        product.description = request.data.get("description", product.description)
        product.stock = request.data.get("stock", product.stock)
        product.img_url = request.data.get("img_url", product.img_url)
        product.save()
        return Response({"message": "Product updated successfully"})
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

# Delete product (admin only)
@api_view(['DELETE'])
def deleteProduct(request, pname):
    uname = request.data.get('username')
    try:
        User = UserData.objects.get(username=uname)
        if User.usertype != 'admin':
            return Response({'error': 'Only admin can delete products'}, status=403)
    except UserData.DoesNotExist:
        return Response({'error': 'Invalid Product'}, status=400)

    try:
        product = Product.objects.get(pname=pname)
        product.delete()
        return Response({'message': 'Product deleted successfully'})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
