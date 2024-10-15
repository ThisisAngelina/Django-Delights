from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from datetime import datetime
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from .forms import *


#Home page
@login_required
def home_view(request):
    
    context = {}

    #calculating tbis month's revenue, expenses and profit to display on the home page
    context['profit_data'] = []
    
    now = datetime.now()
    revenue = 0
    cost = 0
    purchases = Purchase.objects.prefetch_related('menu_items__ingredients').filter(date__month=now.month, date__year=now.year)
        
    #loop over the purchases in the given month
    for purchase in purchases:
        revenue += purchase.total

        for menu_item in purchase.menu_items.all():
            recipe_requirements = RecipeRequirement.objects.filter(menu_item=menu_item)
            for requirement in recipe_requirements:
                ingredient = requirement.ingredient
                quantity_needed = requirement.quantity
                # Calculate the cost based on quantity used and ingredient price
                cost += ingredient.price * quantity_needed

    profit = revenue - cost
    context['revenue'] = revenue
    context['cost'] = cost
    context['profit'] = profit

    #geting hold of the user that is logged in
    context['username'] = request.user.username

    return render(request, 'inventory/home.html', context)


#Ingredient view: An inventory of different Ingredients, their available quantity, and their prices per unit
class InventoryList(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = 'inventory/inventory.html' 
    context_object_name = 'ingredients'

#Add a new ingredient
class InventoryCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    fields = '__all__'
    template_name = 'inventory/inventory_new.html'
    success_url = reverse_lazy('inventory')

#Update inventory view: allows the restaurant owner to change the quantity of the ingredient manually (if an ingredient goes bad or if the restaurant get a supply of the ingredients)
class InventoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = '__all__'
    template_name = 'inventory/inventory_update.html'
    success_url = reverse_lazy('inventory')

#Recipes view: A list of the restaurant’s MenuItems, and the price set for each entry
class MenuList(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = 'inventory/menu.html'
    context_object_name = 'menu_items'

#Add a new menu item using formset: add the menu items and the associated ingredients + quantities 
class MenuCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'inventory/menu_new.html'
    success_url = reverse_lazy('menu')

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        RecipeFormSet = inlineformset_factory(MenuItem, RecipeRequirement, form=RecipeRequirementForm, extra=4, can_delete=True)

        if self.request.POST:
            context['formset'] = RecipeFormSet(self.request.POST)
        else:
            context['formset'] = RecipeFormSet()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = self.object  
            formset.save()

        return response
    
#Update an existing menu item using formset: edit the menu item and the associated ingredients + quantities 
class MenuUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'inventory/menu_update.html'
    success_url = reverse_lazy('menu')

    def get_context_data(self, **kwargs):
        # Call the parent implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Adding a custom inline formset model to display the Ingredients next to the relative menu item
        RecipeFormSet = inlineformset_factory(MenuItem, RecipeRequirement, form=RecipeRequirementForm, extra=0, can_delete=True)

        # Initialize the formset with the MenuItem instance
        if self.request.POST:
            context['formset'] = RecipeFormSet(self.request.POST, instance=self.object)  # Bind the formset with POST data
        else:
            context['formset'] = RecipeFormSet(instance=self.object)  # Load the existing data into the formset

        return context

    def form_valid(self, form):
        # Save the MenuItem first
        response = super().form_valid(form)

        # Handle the RecipeRequirement formset
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = self.object  # Associate the RecipeRequirements with the updated MenuItem
            formset.save()

        return response


#Ingredients view: A list of the ingredients that each menu item requires (RecipeRequirements)
@login_required
def recipe_list(request):
    menu_items = MenuItem.objects.prefetch_related('reciperequirement_set')
    recipes = [(menu_item, RecipeRequirement.objects.filter(menu_item=menu_item)) for menu_item in menu_items]
    return render(request, 'inventory/recipes.html', {'recipes': recipes})

#Purchases view: A log of all Purchases made at the restaurant: purchase date, menu items in the purchase and the purchase total
@login_required
def purchase_list(request):
    purchases = Purchase.objects.prefetch_related('menu_items').all()
    context = {
        'purchases' : purchases
    }
    return render(request, 'inventory/purchases.html', context)

#Profit and Loss view: view revenue, costs, profit per month - for the current year
@login_required
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
                recipe_requirements = RecipeRequirement.objects.filter(menu_item=menu_item)
                for requirement in recipe_requirements:
                    ingredient = requirement.ingredient
                    quantity_needed = requirement.quantity
                    # Calculate the cost based on quantity used and ingredient price
                    cost += ingredient.price * quantity_needed

        profit = revenue - cost
        profit_data.append({
            'year': year, 
            'month' : datetime(year, i, 1).strftime('%B'),
            'revenue' : revenue,
            'cost': cost,
            'profit': profit
        } )
    return render(request, 'inventory/profit.html', {'profit_data': profit_data})


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    
    model = Purchase
    form_class = NewPurchaseForm
    template_name = 'inventory/purchase_new.html'
    success_url = reverse_lazy('purchases')

    #override this built-in method to run addiitonal calculations when the form is submitted but before it is saved
    def form_valid(self, form):
        menu_items = form.cleaned_data.get('menu_items')

        for menu_item in menu_items:
            recipe_requirements = RecipeRequirement.objects.filter(menu_item=menu_item)
            for requirement in recipe_requirements:
            
                ingredient = requirement.ingredient #access the inventory
                quantity_needed = requirement.quantity #access the recipes
                
                # Make sure we have enough of the ingredient in stock
                if ingredient.quantity >= quantity_needed:
                    ingredient.quantity -= quantity_needed
                    ingredient.save() #update the inventory
                else:
                    message = f"Not enough {ingredient.name} in stock to fulfill the order for {menu_item.name}"
                    return self.render_to_response(self.get_context_data(form=form, message=message))
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = kwargs.get("message", "")
        return context

