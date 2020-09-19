from django.contrib import admin
from .models import Customer,Product,Order,OrderItem,shippingaddress,Orderconfirmed,Categorys,Contact
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(shippingaddress)
admin.site.register(Orderconfirmed)
admin.site.register(Categorys)
admin.site.register(Contact)
