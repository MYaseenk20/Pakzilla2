from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    path('CheckOut/', views.CheckOut, name='CheckOut'),
]