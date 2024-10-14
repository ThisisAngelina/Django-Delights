from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
    path ('', include('authenticate.urls'))
]
#    path ('', include('django.contrib.auth.urls')),