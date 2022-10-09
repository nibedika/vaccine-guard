from django.urls import path
from apps.access_apps.access import views
 
urlpatterns = [
    path('sign-up/', views.Access.sign_up, name='sign_up'),
    path('sign-in/', views.Access.sign_in, name='sign_in'),
    path('sign-out/', views.Access.sign_out, name='sign_out'),
    path('user-sign-up/', views.Access.user_sign_up, name='user_sign_up'),
    path('user-sign-in/', views.Access.user_sign_in, name='user_sign_in'),
    path('user-confirmation/<emailCode>/<email>/', views.Access.user_confirmation, name='user_confirmation'),
    path('user-sign-out/', views.Access.user_sign_out, name='user_sign_out'),

    path('admin-panel/', views.Access.home, name='home'),
    path('', views.Access.website, name='website'),
    path('view-profile/', views.Access.view_profile, name='view_profile'),
    path('edit-profile/', views.Access.edit_profile, name='edit_profile'),
]