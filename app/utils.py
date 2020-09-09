import json
from .models import *
def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    orders = {'get_cart_item': 0, 'get_cart_total': 0, 'shipping': False}
    orderitem = orders['get_cart_item']
    for i in cart:
        try:
            orderitem += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']
            orders['get_cart_item'] += cart[i]['quantity']
            orders['get_cart_total'] += total

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'ImageUrl': product.ImageUrl,
                },
                'quantity': cart[i]['quantity'],
                'Total_of_item': total
            }
            items.append(item)
            if product.digital == False:
                orders['shipping']=True
        except:
            pass


    return {'orderitem':orderitem,'orders':orders,'items':items}

def Viewdata(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        orders,create=Order.objects.get_or_create(customer=customer,complete=False)
        items=orders.orderitem_set.all()
        orderitem=orders.get_cart_item
    else:
        cookieData=cookieCart(request)
        orderitem=cookieData['orderitem']
        orders=cookieData['orders']
        items=cookieData['items']
    return{
        'orders':orders,
        'items':items,
        'orderitem':orderitem
    }