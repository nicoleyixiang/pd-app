import json
from . models import *

def cookieCart(request):
    try:
        # Try to create a cookieCart 
        cart = json.loads(request.COOKIES['cart'])
    except:
        # If exception occurs, set cart to an empty dictionary 
        cart = {}
        print('Cart:', cart)

    # Set standard values
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'get_total_cost':0}
    cartItems = order['get_cart_items']
    item = {}

    # Loop through each item in the cart 
    for i in cart:
        try:
            # Update cartItems to include the newest number of items in the cart 
            cartItems += cart[i]["quantity"]

            # Get the product using the id 
            product = Product.objects.get(id=i)

            # order['get_cart_total'] += total
            # order['get_cart_items'] += cart[i]["quantity"]

            # Create an item dictionary that stores 
            # key value pairs of relevant information 
            # of the Product
            item = {
                'product':{
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                    'category': product.category.name,
                },
                'get_unit_cost': product.get_unit_cost,
                'quantity':cart[i]["quantity"],
            }
            # Add the item to a list of items  
            items.append(item)
        except:
            pass
    # Return a dictionary of all necessary data 
    return {'cartItems': cartItems, 'order':order, 'item':item}

def calculatorData(request):
    # If the user is authenticated 
    if request.user.is_authenticated:
        student = request.user.student
        order, created = Order.objects.get_or_create(student=student, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        name = items[0].get_product_name
        product = Product.objects.get(name=name)
    # If the user is a guest visitor
    else:
        # Create a cookie cart (guest cart) and bind the data to cookieData
        cookieData = cookieCart(request)
        # Retrieve the cartItems, order, and item in the cookieData 
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        item = cookieData['item']

        # Retrieve the product id of the item retrieved 
        productId = item['product']['id']
        # Retrieve the Product with the corresponding product id 
        product = Product.objects.get(id=productId)

    return {'cartItems':cartItems ,'order':order, 'product':product, 'item':item}
