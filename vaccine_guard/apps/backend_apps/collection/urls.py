from django.urls import path
from apps.backend_apps.collection import views
 
urlpatterns = [
    path('add-collection/', views.Collection.add_collection, name='add_collection'),
    path('all-collection/', views.Collection.all_collection, name='all_collection'),
    path('delete-collection/<id>/', views.Collection.delete_collection, name='delete_collection'),
]