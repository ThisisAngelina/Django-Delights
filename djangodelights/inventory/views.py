from django.shortcuts import render
from django.views.generic import ListView
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement


#Ingredient view: An inventory of different Ingredients, their available quantity, and their prices per unit
class InventoryList(ListView):
    model = Ingredient
    template_name = 'inventory/inventory.html' 
    context_object_name = 'ingredients'

#Recipes view: A list of the restaurant’s MenuItems, and the price set for each entry
class MenuList(ListView):
    model = MenuItem
    template_name = 'inventory/menu.html'
    context_object_name = 'menu_items'



#TODO class PurchaseCreate(CreateView):
'''
TODO record a new purchase, calculating the purchase total
TODO subtract ingredients from Ingredient
TODO update revenue, costs and profit
TODO redirect to the purchase list
'''

