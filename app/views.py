from django.shortcuts import render
from .models import Product,Order,OrderItem,shippingaddress,Customer,Orderconfirmed
from django.http import JsonResponse
import datetime
import json
from .utils import cookieCart,Viewdata
# Create your views here.
def home(request):
    products = Product.objects.all()
    viewdata=Viewdata(request)
    orderitem=viewdata['orderitem']
    items=viewdata['items']
    orders=viewdata['orders']

    context={'products':products,'orderitem':orderitem,'items':items,'orders':orders}
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
