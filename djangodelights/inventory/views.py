from django.shortcuts import render
from django.views.generic import ListView
from .models import Ingredient, Purchase, RecipeRequirement


#Ingredient view
class InventoryList(ListView):
    model = Ingredient
    template_name = 'inventory/inventory.html' 
    context_object_name = 'ingredients'




#TODO class PurchaseCreate(CreateView):
'''
TODO record a new purchase, calculating the purchase total
TODO subtract ingredients from Ingredient
TODO update revenue, costs and profit
TODO redirect to the purchase list
'''

