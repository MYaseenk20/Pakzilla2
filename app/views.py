from django.shortcuts import render,redirect
from .models import Product,Order,OrderItem,shippingaddress,Customer,Orderconfirmed,Categorys,Contact
from django.http import JsonResponse
import datetime
import json
from .utils import cookieCart,Viewdata
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate

# Create your views here.
def home(request):
    products = None

    categorys=Categorys.objects.all()
    categoryID=request.GET.get('category')
    if categoryID:
        products = Product.objects.filter(categorys=categoryID)
    else:
        products = Product.objects.all()

    viewdata=Viewdata(request)
    orderitem=viewdata['orderitem']
    items=viewdata['items']
    orders=viewdata['orders']

    context={'products':products,'orderitem':orderitem,'items':items,'orders':orders,'categorys':categorys}
    return render(request,'app/store.html',context)
def cart(request):
    viewdata = Viewdata(request)
    orderitem = viewdata['orderitem']
    items = viewdata['items']
    orders = viewdata['orders']

    context={'items':items,'orders':orders,'orderitem':orderitem}

    return render(request,'app/cart.html',context)
def checkout(request):
    viewdata=Viewdata(request)
    orderitem=viewdata['orderitem']
    items=viewdata['items']
    orders=viewdata['orders']
    context={'items':items,'orders':orders,'orderitem':orderitem}
    return render(request,'app/checkout.html',context)

def update_item(request):
    data=json.loads(request.body)
    productId=data['productid']
    action=data['action']

    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,create=Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,create=OrderItem.objects.get_or_create(order=order,product=product,customer=customer)

    if action == 'add':
        orderitem.quantity=(orderitem.quantity+1)

    elif action == 'remove':
        orderitem.quantity=(orderitem.quantity-1)
    orderitem.save()

    if orderitem.quantity<=0:
        orderitem.delete()



    return JsonResponse('item was added',safe=False)


def CheckOut(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order,create=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()

        for item in items:
            Orderconfirmed.objects.create(
                customer=customer,
                order=order,
                product=item.product,
            )

    else:
        print('Cookies',request.COOKIES)
        name=data['form']['name']
        email=data['form']['email']
        print(email)
        viewdata=Viewdata(request)
        items=viewdata['items']
        customer,create=Customer.objects.get_or_create(
            email=email,
            name=name,
        )
        customer.name=name
        customer.save()
        order=Order.objects.create(
            customer=customer,
            complete=False
            )
        for item in items:
            product=Product.objects.get(id=item['product']['id'])
            orderitem=OrderItem.objects.create(
                customer=customer,
                product=product,
                order=order,
                quantity=item['quantity']
            )
            Orderconfirmed.objects.create(
                customer=customer,
                order=order,
                product=product,
                quantity=item['quantity']
            )
    order.transaction_id = transaction_id
    total = float(data['form']['total'])
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
        shippingaddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )


    return JsonResponse('Order Submitted',safe=False)

#
def category(request):
    products = None
    viewdata=Viewdata(request)
    orderitem=viewdata['orderitem']

    categorys=Categorys.objects.all()
    categoryID=request.GET.get('category')
    if categoryID:
        products = Product.objects.filter(categorys=categoryID)
    else:
        products = Product.objects.all()
    context={'categorys':categorys,'products':products,'orderitem':orderitem}
    return render(request,'app/category.html',context)




def ProductDetail(request,pk):
    product=Product.objects.get(id=pk)
    products=Product.objects.all()
    viewdata=Viewdata(request)
    orderitem=viewdata['orderitem']
    context={'orderitem':orderitem,'product':product,'products':products}
    return render(request,'app/product.html',context)


def Search(request):
    qureyset_list=Product.objects.all()
    if 'Search' in request.GET:
        Search=request.GET['Search']
        if Search:
            qureyset_list=qureyset_list.filter(name__icontains=Search)
    viewdata=Viewdata(request)
    orderitem=viewdata['orderitem']
    context={'orderitem':orderitem,'qureyset_list':qureyset_list}
    return render(request,'app/Search.html',context)

def Contact(request):
    if request.method == 'POST':
        message=request.POST.get('message')
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        print(message)
        print(name)
        print(email)
        print(subject)
        Contact.objects.create(message=message,name=name,Email=email,subject=subject)
        return redirect('store')
    return render(request,'app/contact.html')
def Signup(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'This username is already taken')
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'This email is already taken')
                    return redirect('signup')
                else:
                    user=User.objects.create_user(username=username,email=email,password=password1)
                    user.save()
                    return redirect('login')
                    messages.success(request,'Your account Has been created ')

        return redirect('store')
    return render(request,'app/signup.html')

def loginuser(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        print(username)
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('store')

    return render(request,'app/login.html')


