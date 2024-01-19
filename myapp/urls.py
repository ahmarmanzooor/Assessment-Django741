# from django.urls import path
# from .views import RegisterView, LoginView, LogoutView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
# ]

from django.contrib import admin
from django.urls import path
from .views import product_list, product_detail, seller_list, seller_detail,login_view,register_view,logout_view,LandingPage,add_product

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_product/', add_product, name='add-product'),
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
    path('sellers/', seller_list, name='seller-list'),
    path('sellers/<int:pk>/', seller_detail, name='seller-detail'),
    path('registerPostman/', register_view, name='register'),
    path('loginPostman/', login_view, name='login'),
    path('logoutPostman/', logout_view, name='logout'),
    path('', LandingPage, name='create_product'),

    
   
]