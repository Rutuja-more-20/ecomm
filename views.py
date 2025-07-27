from django.shortcuts import render
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from users.models import UserData
from django.http import HttpResponse
from rest_framework import status
from users.serializers import UserDataSerializer

# Create your views here.
from django.contrib.auth import logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserData

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = UserData.objects.get(username=username, password=password)
    except UserData.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=401)

    # Create JWT tokens manually for your custom user model
    refresh = RefreshToken.for_user(user)

    # Store custom claim like user ID
    refresh['user_id'] = user.id
    refresh['username'] = user.username

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    logout(request)
    return Response({"message": "Logout successful"})

#read all data from userdata table
@api_view(['GET'])
def getAllUsers(request):
     queryset=UserData.objects.all().values()
     users=list(queryset)
     return Response(users)

#get details by username
@api_view(['GET'])
def getUser(request, username):
    user = UserData.objects.get(username=username)
    data = {
        'username': user.username,
        'password': user.password,
        'mobno': user.mobno,
        'email': user.email,
        'usertype':user.usertype
    }
    return Response(data)

#add user
@api_view(['POST'])
def registeruser(request):
    username = request.data.get('username')

    # Check if username already exists
    if UserData.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'})

    # Serialize and validate the input
    serializer = UserDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'})

    # Return validation errors
    return Response(serializer.errors)
    
#login user
@api_view(['POST'])
def loginUser(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = UserData.objects.get(username=username, password=password)
        # Return user type (assuming you have a field `usertype`)
        return Response({
            "message": "Login successful",
            "usertype": user.usertype  # e.g., "admin" or "user"
        })
    except UserData.DoesNotExist:
        return Response({"error": "Invalid credentials"})

    
#delete user
@api_view(['DELETE'])
def deleteUser(request,userfromclient):
    try:
        User=UserData.objects.filter(username=userfromclient)
        if User.exists():
            User.delete()
            return Response({'message':'record deleted'})
        else:
            return Response({'message':'record not found'})
    except Exception as e:
        return Response({'message':'error occured'})

#update user
@api_view(['PUT'])
def updateUser(request):
    data = request.data
    username = data.get("username")
    try:
        user = UserData.objects.get(username=username)
        
        user.email = data.get("email", user.email)
        user.mobno = data.get("mobno", user.mobno)
        user.password = data.get("password", user.password)
        user.usertype = data.get("usertype", user.usertype)
        
        user.save()
        return Response({"message": "User updated successfully"})

    except:
        return Response({"error": "User not found"})

