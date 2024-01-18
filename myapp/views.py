
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Seller
from .serializers import ProductSerializer, SellerSerializer
# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required



from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from .forms import ProductForm

@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password:
        return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the username is already taken
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new user using Django's default authentication
    user = User.objects.create_user(username=username, password=password, email=email)

    return Response({'message': 'Registration successful.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user using Django's default authentication
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Login the user using Django's login function
        login(request, user)

        return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@login_required
def logout_view(request):
    # Logout the user using Django's logout function
    logout(request)

    return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)

# # User logout class base view

# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         refresh_token = request.data.get('refresh_token')

#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#         except Exception:
#             return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)

#         return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)




@api_view(['GET', 'POST'])
@login_required
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a product
@api_view(['GET', 'PUT', 'DELETE'])
@login_required
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# List all sellers or create a new seller
@api_view(['GET', 'POST'])
@login_required
def seller_list(request):
    if request.method == 'GET':
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a seller
@api_view(['GET', 'PUT', 'DELETE'])
@login_required
def seller_detail(request, pk):
    try:
        seller = Seller.objects.get(pk=pk)
    except Seller.DoesNotExist:
        return Response({'error': 'Seller not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SellerSerializer(seller)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SellerSerializer(seller, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        seller.delete()
        return Response({'message': 'Seller deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    
    
    
    
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            # You can redirect to a success page or display a success message
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'create_product.html', {'form': form})    