from django.urls import path
from . import views

urlpatterns = [path('inventory/', views.InventoryList.as_view(), name='inventory'),
            path('menu/', views.MenuList.as_view(), name='menu'),
            path('recipes/', views.recipe_list, name='recipes'),
            path('purchases/', views.purchase_list, name='purchases')
               ]
'''

    path('', views.home, name='home'),


    
    path('profit/', views.purchases_view, name='profit'),
    path('login/', views.login_view, name='login'),
]

'''