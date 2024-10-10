from django.shortcuts import render
from django.views.generic import ListView
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from datetime import datetime


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

#Purchases view: A log of all Purchases made at the restaurant: purchase date, menu items in the purchase and the purchase total
def purchase_list(request):
    purchases = Purchase.objects.prefetch_related('menu_items').all()
    context = {
        'purchases' : purchases
    }
    return render(request, 'inventory/purchases.html', context)

#Profit and Loss view: view revenue, costs, profit per month - for the current year
def profit_view(request):
    now = datetime.now()
    year = now.year
    profit_data = []

    #create a dictionary of values for every month of the year 
    for i in range(1, now.month+1):
        revenue = 0
        cost = 0
        purchases = Purchase.objects.prefetch_related('menu_items__ingredients').filter(date__month=i, date__year=year)
        
        #loop over the purchases in the given month
        for purchase in purchases:
            revenue += purchase.total

            for menu_item in purchase.menu_items.all():
                ingredients = menu_item.ingredients.all()
                for ingredient in ingredients:
                    cost += ingredient.price
        profit = revenue - cost
        profit_data.append({
            'year': year, 
            'month' : datetime(year, i, 1).strftime('%B'),
            'revenue' : revenue,
            'cost': cost,
            'profit': profit
        } )
    return render(request, 'inventory/profit.html', {'profit_data': profit_data})




#TODO class PurchaseCreate(CreateView):
'''
TODO record a new purchase, calculating the purchase total
TODO subtract ingredients from Ingredient
TODO update revenue, costs and profit
TODO redirect to the purchase list
'''

