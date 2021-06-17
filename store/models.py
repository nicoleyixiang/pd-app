from django.db import models
from django.contrib.auth.models import User

# The model for a Category. Each Product
# is associated with one of the Categories. 
# The standard four categories are Sheets (planks, 
# cardboard, paper, etc.), Liquids (glue, varnishes, etc.),
# Components (screws, clock mechanisms, etc.),
# and Lengths (pipes, rope, wire, etc.) 
class Category(models.Model):
    name = models.CharField(max_length=200, default='', blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    # Returns the image that has been uploaded by the admin.    
    # If no image was uploaded, the program produces a placeholder.
    # This ensures program will not crash when no image is available. 
    @property
    def imageURL(self):
        # Try to retrieve the image uploaded to the database 
        try:
            # Set url to the image URL retrieved
            url = self.image.url
        # If an error occurs in the retrieval process (ie. if no image is available)
        except:
            # Set url to an empty string
            url = ''
        # Return url
        return url
    pass 

# The model for a Student (ie. the user).
# Stores all the relevant information of 
# a registered user. Currently not needed 
# to use to website but login features
# can be added in the future. 
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

# The model for a Product (ie. a material item). 
# Stores all the relevant information to be 
# displayed and used in the program. 
class Product(models.Model):
    name = models.CharField(max_length=200, default='', blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=20, blank=False)
    length = models.IntegerField(blank=True, default=0)
    width = models.IntegerField(blank=True, default=0)
    volume = models.IntegerField(blank=True, default=0)
    quantity = models.IntegerField(blank=True, default=1)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default='', blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name

    # Returns the image that has been uploaded by the admin.
    # If no image was uploaded, the program produces a placeholder.
    # This ensures program will not crash when no image is available. 
    @property
    def imageURL(self):
        # Try to retrieve the image uploaded to the database 
        try:
            # Set url to the image URL retrieved
            url = self.image.url
        # If an error occurs in the retrieval process (ie. if no image is available)
        except:
            # Set url to an empty string 
            url = ''
        # Return url 
        return url
    
    # Returns the total size of the material 
    # (eg. a 500mm by 400mm wood plank would 
    # have a size of 200,000mm^2).
    # To be used for calculating the "per 
    # unit cost" of the material. 
    @property
    def get_total_size(self):
        # Check if the width was inputted as 0
        if self.width == 0:
            # Check if the length was also inputted as 0
            if self.length == 0:
                # Check if the volume was also inputted as 0
                if self.volume == 0:
                    # If all pass, then the material is a component. Set total to quantity.  
                    total = self.quantity
                # If the volume is not 0 
                else:
                    # The material is a liquid. Set total to volume. 
                    total = self.volume
            # If the length is not 0 
            else:
                # The material is a length. Set total to length. 
                total = self.length
        # If the length and width are not 0 
        elif self.width != 0 and self.length != 0:
            # 
            total = self.length * self.width
        # If something goes wrong and all of the above are false 
        else:
            # Set total to 0 (a 0 value for size will notify user in views.py on line 155 that something went wrong).
            total = 0
        # Return the total size of the material 
        return total

    # Returns the per unit cost of the material
    # based on the total price / total size 
    # of the product when it was purchased
    # (eg. how much would one ml of glue cost).
    # To be used with the user's inputs for calculations.
    @property
    def get_unit_cost(self):
        # Retrieve the total size of the material 
        size = self.get_total_size
        # If the size is equal to 0.
        if size == 0:
            # Set cost to 0 (a 0 value for cost will notify user in views.py on line 155 that something went wrong).
            cost = 0
        else:
            # Set cost to the total price divided by the total size to get the "per unit cost".
            cost = self.price / size 
        # Return the per unit cost of the material 
        return cost

class Order(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems])
        return total 

    @property
    def get_cart_items(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total 

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    calculated_cost = models.FloatField(default=0, null=True, blank=True)

    @property
    def get_product_name(self):
        name = self.product.name
        return name

    @property 
    def get_total(self):
        total = self.product.get_unit_cost * self.quantity
        return total

    @property
    def get_unit_cost(self):
        return self.product.get_unit_cost