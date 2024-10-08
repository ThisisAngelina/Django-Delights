from django.shortcuts import render
from django.views.generic import ListView
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase


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


#Ingredients view: A list of the ingredients that each menu item requires (RecipeRequirements)
def recipe_list(request):
    menu_items = MenuItem.objects.prefetch_related('reciperequirement_set')

    recipes = [(menu_item, RecipeRequirement.objects.filter(menu_item=menu_item)) for menu_item in menu_items]
    
    return render(request, 'inventory/recipes.html', {'recipes': recipes})

#TODO class PurchaseCreate(CreateView):
'''
TODO record a new purchase, calculating the purchase total
TODO subtract ingredients from Ingredient
TODO update revenue, costs and profit
TODO redirect to the purchase list
'''

