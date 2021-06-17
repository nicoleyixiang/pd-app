from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from . models import *
from . utils import cookieCart
from . forms import *
from django.views.generic.list import ListView   
from django.contrib import messages
from math import log10, floor

def store(request):
    # If the user is an authenticated user
    if request.user.is_authenticated:
        student = request.user.student
        order, created = Order.objects.get_or_create(student=student, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    # If the user is a guest user
    else:
        # Create a cookie cart (guest cart) and bind the data to cookieData
        cookieData = cookieCart(request)
        # Retrieve the cartItems number from the cookieData
        cartItems = cookieData['cartItems']

    # Retrieve all the Category objects 
    categories = Category.objects.all()

    # Pass the relevant information to the store page (main landing page)
    context = {'categories':categories, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def updateItem(request):
    # Retrieve the json request data 
	data = json.loads(request.body)

    # Obtain the relevant information from the data passed through 
	productId = data['productId']
	action = data['action']

    # Set standard variables necessary for a logged in user 
	student = request.user.student
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(student=student, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # If the action is "add"
	if action == 'add':
        # Add one to the quantity of the orderItem
		orderItem.quantity = (orderItem.quantity + 1)
    # If the action is "remove"
	elif action == 'remove':
        # Subtract one from the quantity of the orderItem
		orderItem.quantity = (orderItem.quantity - 1)

    # Save the orderItem in the database
	orderItem.save()

    # If the orderItem is less than or equal to 0
	if orderItem.quantity <= 0 :
        # Delete the orderItem off the database
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def category(request):
    # Retrieve the name of the category from the POST request.
    # Does not affect the state of the system (does not change database)
    category_name = request.POST.get('category', None)
    # Retrieve the Category object with the corresponding category name
    category = Category.objects.get(name=category_name)
    # Retrieve all the Products that are associated with that Category
    # Order in alphabetical order by name 
    products = Product.objects.filter(category=category).order_by('name')
    # Source for the alphbetical order code:
    # https://stackoverflow.com/questions/16778819/django-how-to-sort-objects-alphabetically-by-first-letter-of-name-field/16779964
    
    # Send the collection of Products and the category name as a context dictionary 
    context = {'products':products, 'title':category_name}
    # Render the view using the information 
    return render(request, 'store/category.html', context)

def calculator(request):
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

    # Initialize some standard values to display on the page in order to prevent errors 
    number = 0
    size = 0
    calculated_price = 0.00
    
    # Set and create the form based on the category type. Set to standard product form if no category matches
    if product.category.name == 'Sheets':
        form = SheetsForm(request.POST)
    elif product.category.name == 'Lengths':
        form = LengthsForm(request.POST)
    elif product.category.name == 'Components':
        form = ComponentsForm(request.POST)
    elif product.category.name == 'Liquids':
        form = LiquidsForm(request.POST)
    else:
        form = ProductForm(request.POST)

    # If the form button is pressed and the form is valid
    if request.method == "POST":
        if form.is_valid():
            # Check if the length of the form dictionary is 3 (ie. is the form for a sheet product?).
            if len(form.cleaned_data) == 3:
                # Set the size to width x length (ie. area), as inputted by the user. 
                size = form.cleaned_data["length"] * form.cleaned_data["width"]
                # Check if the desired length is larger than both the database-stored length and width values for the sheet.
                if form.cleaned_data["length"] > product.length and form.cleaned_data["length"] > product.width:
                    # Send an error message.
                    messages.warning(request, 'Error: Your length is too long to fit the given material. Please input a shorter length.')
                # Check if the desired width is larger than both the database-stored length and width values for the sheet.
                elif form.cleaned_data["width"] > product.length and form.cleaned_data["width"] > product.width:
                    # Send an error message.
                    messages.warning(request, 'Error: Your width is too wide to fit the given material. Please input a smaller width.')
            # Check if the length of the form dictionary is 2 (ie. is the form for a liquid or length product?).
            elif len(form.cleaned_data) == 2:
                # Try to set the size to the inputted volume from the form.
                try:
                    size = form.cleaned_data["volume"]
                # If an exception occurs, it means the Product is a 'length'. Set the size to the inputted length. 
                except:
                    size = form.cleaned_data["length"]
            # Check if the length of the form dictionary is 1 (ie. is the form for a component product?).
            elif len(form.cleaned_data) == 1:
                # Set the size to 1 (components are measured only by quantity, size does not change). 
                size = 1
            # If none of the above are true, then something has been passed through incorrectly. 
            else:
                # Send an error message. 
                messages.warning(request, 'Error: Something went wrong in your inputs. Please contact an administrator.')

            # If the total size or the per unit cost of the material is less than or equal to zero
            if product.get_total_size <= 0 or product.get_unit_cost <= 0:
                # Send an error message 
                messages.warning(request, 'Error: Material data was stored/inputted incorrectly. Please contact your PD teacher or an administrator.')
            # If the user's desired size of the material is larger than the total size of the product:
            elif size > product.get_total_size:
                # Send an error message.
                messages.warning(request, 'Error: Your selected dimensions are larger than the material itself. Please input smaller values.')
            # Or if the quantity the user inputted is abnoramlly large:
            elif form.cleaned_data['quantity'] > 1000:
                # Send an error message.
                messages.warning(request, 'Error: You inputted an abnormally large quantity. Please input a smaller value or contact your PD teacher.')
            # If all error checking processes above pass:
            else: 
                # Retrieve the quantity (ie. how many copies of this size of this material does the user need?)
                number = form.cleaned_data['quantity']
                # Multiply the size by the quantity they inputted to find the total amount of material the user needs.
                total_units = size * number

                # Check if the per unit cost of the material less than one (a fractional value)?
                if item['get_unit_cost'] < 1:
                    # Round to 1 significant figure 
                    per_unit_cost = round(item['get_unit_cost'], -int(floor(log10(abs(item['get_unit_cost'])))))
                    # Source: https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python 
                else:
                    # Otherwise, set per_unit_cost to the per unit cost of the material (eg. the cost of 1mm of rope)
                    per_unit_cost = item['get_unit_cost']
                # Calculate the price of the material by multiplying by the per unit cost of the material. 
                calculated_price = total_units * per_unit_cost

                # Last error check: checking if the price is a negative number (ie. invalid cost)
                if calculated_price <= 0:
                    # Send an error message.
                    messages.warning(request, 'Error: Negative number detected. Please reinput your values.')
        else:
            # Set standard values to prevent the website from crashing if the form malfunctions. 
            number = 0
            size = 0
            calculated_price = 0.00

    # Pass relevant information to the calculator page
    context = {'product': product, 'form': form, 'price': calculated_price, 'number': number, 'size': size} 
    return render(request, 'store/calculator.html', context)