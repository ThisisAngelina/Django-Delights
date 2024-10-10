from django.urls import path
from . import views

urlpatterns = [path('inventory/', views.InventoryList.as_view(), name='inventory'),
            path('menu/', views.MenuList.as_view(), name='menu'),
            path('recipes/', views.recipe_list, name='recipes'),
            path('purchases/', views.purchase_list, name='purchases'),
            path('profit/', views.profit_view, name='profit'),
            path('inventory/<int:pk>/edit/', views.InventoryUpdateView.as_view(), name='inventory_update'),
               ]
'''

    path('', views.home, name='home'),


    
   
    path('login/', views.login_view, name='login'),
]

'''