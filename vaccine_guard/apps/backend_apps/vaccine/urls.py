from django.urls import path
from apps.backend_apps.vaccine import views
 
urlpatterns = [
    path('all-vaccine/', views.Vaccine.all_vaccine, name='all_vaccine'),
    path('view-vaccine/<id>/', views.Vaccine.view_vaccine, name='view_vaccine'),
    path('view-user-vaccine/<id>/', views.Vaccine.view_user_vaccine, name='view_user_vaccine'),
    path('edit-vaccine/<id>/', views.Vaccine.edit_vaccine, name='edit_vaccine'),
]