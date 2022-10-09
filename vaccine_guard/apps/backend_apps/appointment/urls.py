from django.urls import path
from apps.backend_apps.appointment import views
 
urlpatterns = [
    path('add-appointment/', views.Appointment.add_appointment, name='add_appointment'),
    path('all-appointment/', views.Appointment.all_appointment, name='all_appointment'),
    path('edit-appointment/<id>/', views.Appointment.edit_appointment, name='edit_appointment'),
    path('delete-appointment/<id>/', views.Appointment.delete_appointment, name='delete_appointment'),
]