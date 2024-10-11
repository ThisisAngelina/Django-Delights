from django import forms
from .models import MenuItem, RecipeRequirement, Ingredient

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price']

class RecipeRequirementForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ['ingredient', 'quantity']