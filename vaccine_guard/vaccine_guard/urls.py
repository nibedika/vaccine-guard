"""restaurant URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# For Media URL
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),

    # Access App's Urls
    path('', include('apps.access_apps.access.urls'), name='access'),

    # Backend App's Urls
    path('appointment/', include('apps.backend_apps.appointment.urls'), name='appointment'),
    path('card/', include('apps.backend_apps.card.urls'), name='card'),
    path('vaccine/', include('apps.backend_apps.vaccine.urls'), name='vaccine'),

    path('supplier/', include('apps.backend_apps.supplier.urls'), name='supplier'),
    path('collection/', include('apps.backend_apps.collection.urls'), name='collection'),
    path('stock/', include('apps.backend_apps.stock.urls'), name='stock'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
