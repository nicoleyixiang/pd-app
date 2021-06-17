from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('update_item/', views.updateItem, name="update_item"),
    path('category/', views.category, name="category"),
    path('calculator/', views.calculator, name="calculator")
]