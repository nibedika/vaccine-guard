from django.urls import path
from apps.backend_apps.stock import views
 
urlpatterns = [
    path('stock/', views.Stock.stock, name='stock'),
]