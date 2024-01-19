
import pdb
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Seller
from .serializers import ProductSerializer, SellerSerializer
# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from django.contrib import messages



from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
# from .forms import ProductForm

@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    # print(username)
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password:
        return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the username is already taken
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new user using Django's default authentication
    user = User.objects.create_user(username=username, password=password, email=email)
    messages.success(request, 'Registration successful. You are now logged in.')
    return redirect('create_product')
    


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
        messages.success(request,  'You are now logged in.')
        

        return redirect('create_product')
    else:
        return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@login_required
def logout_view(request):
    # Logout the user using Django's logout function
    logout(request)

    return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)



def LandingPage(request):
        messages.info(request, 'You are currently logged out.')
        return render(request, 'login.html')  # Redirect to your login

# @api_view(['GET', 'POST'])
# @login_required
# def add_product(request):
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         sellers = Seller.objects.all()
#         return render(request, 'add_product.html', {'categories': categories, 'sellers': sellers})
@login_required
# @api_view(['GET', 'POST'])
def add_product(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        sellers = Seller.objects.all()
        return render(request, 'add_product.html', {'categories': categories, 'sellers': sellers})

    elif request.method == 'POST':
        product_name = request.POST['productName']
        product_description = request.POST['productDescription']
        product_price = request.POST['productPrice']
        category_id = request.POST['category']
        seller_id = request.POST['seller']

        # Assuming you have a Product model with appropriate fields
        product = Product.objects.create(
            name=product_name,
            description=product_description,
            price=product_price,
            category_id=category_id,
            seller_id=seller_id
        )
        return redirect('product-list')  # Replace 'product_list' with the actual URL name for your product list page

    # Handle other cases or provide a default response if needed
    return render(request, 'add_product.html')



@api_view(['GET', 'POST'])
@login_required
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})

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
        return render(request, 'seller_list.html', {'sellers': sellers})


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
    
    
    
    
    
# def create_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # You can redirect to a success page or display a success message
#             return redirect('product_list')
#     else:
#         form = ProductForm()

#     return render(request, 'create_product.html', {'form': form})    