# Django Delights Inventory Management System

This project is a **Django** application designed to manage the inventory, menu items, and purchases of a restaurant. The system also calculates profit and loss based on sales and inventory costs. It was created by ThisisAngelina as part of a Codecademy student project. Access the project using the credentials  **Username**: delights_owner, **Password**: owner0000.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Models](#models)
  - [Ingredient](#ingredient)
  - [MenuItem](#menuitem)
  - [RecipeRequirement](#reciperequirement)
  - [Purchase](#purchase)
- [Views](#views)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [License](#license)

## Project Overview

The Django Delights system provides a web interface where restaurant staff can:

- Track the **inventory** of ingredients, including their quantity and price.
- Manage **menu items**, with each item requiring specific ingredients and quantities.
- Log **purchases**, automatically updating the inventory based on the items sold.
- View **profit and loss reports** for the restaurant, calculated by comparing revenue from purchases and costs of ingredients.

The project consists of two main apps:
1. **Inventory**: Handles the core business logic (inventory, menu items, purchases).
2. **Authenticate**: Manages user authentication (login and logout).

### Features

1. **Inventory Management**:
   - View a list of all ingredients, including available quantities and prices.
   - Add and update ingredients manually (e.g., when ingredients go bad or when new supplies are received).

2. **Menu Management**:
   - View the list of menu items along with their prices.
   - Add new menu items, specifying the required ingredients and quantities for each.
   - Update existing menu items and adjust the required ingredients.

3. **Purchases Management**:
   - Log new purchases, with automatic deductions of ingredient quantities based on recipe requirements.
   - Display a history of purchases including the purchase date, total cost, and items purchased.

4. **Profit and Loss Calculation**:
   - Monthly profit and loss reports based on the sales and ingredient costs for the current year.
   - Reports are displayed on the home page, showing revenue, expenses, and profits.

5. **User Authentication**:
   - The system requires users to log in to access features.
   - Only authenticated users can view and modify data.
   - Pre-configured credentials:
     - **Username**: delights_owner
     - **Password**: owner0000

## Models

### Ingredient
Represents an ingredient in the inventory.
- `name`: The name of the ingredient.
- `quantity`: The available quantity of the ingredient.
- `price`: The price per unit of the ingredient.

### MenuItem
Represents an item on the restaurant’s menu.
- `name`: The name of the menu item.
- `price`: The price of the menu item.
- `ingredients`: Many-to-Many relationship with the `Ingredient` model through the `RecipeRequirement` model.

### RecipeRequirement
Represents the ingredients and quantities required for a `MenuItem`.
- `menu_item`: ForeignKey to `MenuItem`.
- `ingredient`: ForeignKey to `Ingredient`.
- `quantity`: The quantity of the ingredient required for the menu item.

### Purchase
Represents a customer purchase.
- `date`: The date of the purchase.
- `total`: The total amount of the purchase.
- `menu_items`: Many-to-Many relationship with `MenuItem`.

## Views

- **Home Page**: Displays the current month's revenue, cost, and profit.
- **Inventory Management**: 
  - `InventoryList`: Lists all ingredients in the inventory.
  - `InventoryCreateView`: Adds a new ingredient.
  - `InventoryUpdateView`: Updates the quantity and price of an ingredient.
  
- **Menu Management**:
  - `MenuList`: Displays all menu items.
  - `MenuCreateView`: Adds a new menu item with associated ingredients and quantities using formsets.
  - `MenuUpdateView`: Updates an existing menu item with ingredients.

- **Purchase Management**:
  - `purchase_list`: Displays all purchases made at the restaurant.
  - `PurchaseCreateView`: Adds a new purchase and updates the inventory based on the items purchased.

- **Profit and Loss**:
  - `profit_view`: Displays the revenue, cost, and profit for each month of the current year.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd django_delights