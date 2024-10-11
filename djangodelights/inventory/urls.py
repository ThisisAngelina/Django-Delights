from django.urls import path
from . import views

urlpatterns = [path('inventory/', views.InventoryList.as_view(), name='inventory'),
            path('inventory/new', views.InventoryCreateView.as_view(), name='inventory_new'),
            path('inventory/<int:pk>/edit/', views.InventoryUpdateView.as_view(), name='inventory_update'),
            path('menu/', views.MenuList.as_view(), name='menu'),
            path('menu/new', views.MenuCreateView.as_view(), name='menu_new'),
            path('menu/<int:pk>/edit/', views.MenuUpdateView.as_view(), name='menu_update'),
            path('recipes/', views.recipe_list, name='recipes'),
            path('purchases/', views.purchase_list, name='purchases'),
            path('profit/', views.profit_view, name='profit'),
               ]
 