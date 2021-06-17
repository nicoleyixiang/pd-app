from django import forms 
from django.forms import ModelForm
from . models import * 

# Form for sheeets material products
class SheetsForm(forms.Form):
    quantity = forms.IntegerField(label="Quantity", required=True)
    width = forms.IntegerField(label="Width (mm)", required=True)
    length = forms.IntegerField(label="Length (mm)", required=True)

# Form for lengths material products
class LengthsForm(forms.Form):
    quantity = forms.IntegerField(label="Quantity (mm)", required=True)
    length = forms.IntegerField(label="Length (mm)", required=True)

# Form for component material products
class ComponentsForm(forms.Form):
    quantity = forms.IntegerField(label="Quantity", required=True)

# Form for liquid material products 
class LiquidsForm(forms.Form):
    quantity = forms.IntegerField(label="Quantity", required=True)
    volume = forms.IntegerField(label="Volume (ml)", required=True)    

# Standard Product Form 
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['quantity', 'length', 'width', 'volume']