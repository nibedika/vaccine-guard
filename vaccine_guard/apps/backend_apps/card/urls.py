from django.urls import path
from apps.backend_apps.card import views
 
urlpatterns = [
    path('add-card/', views.Card.add_card, name='add_card'),
    path('all-card/', views.Card.all_card, name='all_card'),
    path('view-card/<id>/', views.Card.view_card, name='view_card'),
    path('view-user-card/<id>/', views.Card.view_user_card, name='view_user_card'),
    path('edit-card/<id>/', views.Card.edit_card, name='edit_card'),
    path('delete-card/<id>/', views.Card.delete_card, name='delete_card'),
]