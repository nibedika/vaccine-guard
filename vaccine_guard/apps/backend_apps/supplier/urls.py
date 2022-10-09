from django.urls import path
from apps.backend_apps.supplier import views
 
urlpatterns = [
    path('add-supplier/', views.Supplier.add_supplier, name='add_supplier'),
    path('all-supplier/', views.Supplier.all_supplier, name='all_supplier'),
    path('view-supplier/<id>/', views.Supplier.view_supplier, name='view_supplier'),
    path('edit-supplier/<id>/', views.Supplier.edit_supplier, name='edit_supplier'),
    path('delete-supplier/<id>/', views.Supplier.delete_supplier, name='delete_supplier'),
]