from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    path('CheckOut/', views.CheckOut, name='CheckOut'),
    path('category/', views.category, name='category'),
    path('ProductDetail/', views.ProductDetail, name='ProductDetail'),
    path('Product/<int:pk>/', views.ProductDetail, name='Product'),
    path('Search/', views.Search, name='Search'),
    path('signup/', views.Signup, name='signup'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),

    # path('Contact/', views.Contact, name='Contact'),
]
