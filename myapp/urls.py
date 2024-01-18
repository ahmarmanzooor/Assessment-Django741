# from django.urls import path
# from .views import RegisterView, LoginView, LogoutView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
# ]

from django.contrib import admin
from django.urls import path
from .views import product_list, product_detail, seller_list, seller_detail,login_view,register_view,logout_view,create_product

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
    path('sellers/', seller_list, name='seller-list'),
    path('sellers/<int:pk>/', seller_detail, name='seller-detail'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create_product/', create_product, name='create_product'),
   
]