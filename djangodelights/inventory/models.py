from django.db import models
from django.core.validators import MinValueValidator

class Ingredient(models.Model):
    name = models.CharField (max_length=200)
    quantity = models.FloatField(validators=[MinValueValidator(0.01)])
    price = models.FloatField(validators=[MinValueValidator(0.1)])

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField (max_length=200) 
    price = models.FloatField(validators=[MinValueValidator(0.1)])
    ingredients = models.ManyToManyField(Ingredient, through='RecipeRequirement')

    def __str__(self):
        return f"{self.name} at ${self.price}"

class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(validators=[MinValueValidator(0.01)])  # Quantity required for the recipe must be at least 1

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.menu_item.name}"

class Purchase(models.Model):
    date = models.DateField()
    total = models.FloatField(validators=[MinValueValidator(0.1)])
    menu_items = models.ManyToManyField(MenuItem)

    def __str__(self):
        return f"Purchase on {self.date} for {self.total}"
