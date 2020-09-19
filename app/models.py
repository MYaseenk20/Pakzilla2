from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name


class Categorys(models.Model):
    name=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)
    categorys = models.ForeignKey(Categorys, on_delete=models.CASCADE, default=None,null=True, blank=True)
    price=models.FloatField(null=True)
    image=models.ImageField(null=True,blank=True)
    image=models.ImageField(null=True,blank=True)
    image1=models.ImageField(null=True,blank=True)
    image2=models.ImageField(null=True,blank=True)
    image3=models.ImageField(null=True,blank=True)
    image4=models.ImageField(null=True,blank=True)
    image5=models.ImageField(null=True,blank=True)
    digital=models.BooleanField(default=False,null=False,blank=False)
    newarrival=models.BooleanField(default=False,null=False,blank=False)
    bestseller=models.BooleanField(default=False,null=False,blank=False)
    description=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name
    @property
    def ImageUrl(self):
        try:
            url = self.image.url
        except:
            url=''
        return url

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=False,blank=False)
    transaction_id=models.CharField(max_length=200,null=True)
    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitem=self.orderitem_set.all()
        total=sum([item.Total_of_item for item in orderitem ])
        return total

    @property
    def get_cart_item(self):
        orderitem=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitem ])
        return total
    @property
    def shipping(self):
        shipping=False
        orderitem=self.orderitem_set.all()
        for i in orderitem:
            if i.product.digital == False:
                shipping=True
        return shipping


class OrderItem(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    @property
    def Total_of_item(self):
        total=self.quantity*self.product.price
        return total
class shippingaddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address

class Orderconfirmed(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    message=models.TextField(null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    Email=models.CharField(max_length=200,null=True)
    subject=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
class Car(models.Model):
    message=models.TextField(null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    Email=models.CharField(max_length=200,null=True)
    subject=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name