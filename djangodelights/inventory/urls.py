from django.urls import path
from . import views

urlpatterns = [path('inventory/', views.InventoryList.as_view(), name='inventory')]
'''
urlpatterns = [
    path('', views.home, name='home'),
    path('inventory/', views.InventoryList.as_view(), name='inventory'),
    path('menu/', views.menu_view, name='menu'),
    path('purchases/', views.purchases_view, name='purchases'),
    path('profit/', views.purchases_view, name='profit'),
    path('login/', views.login_view, name='login'),
]

'''