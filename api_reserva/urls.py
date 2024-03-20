
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservas.urls')),
    path('reservas/', include('reservas.urls')),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='accounts')),
    path('accounts/profile/', views.profile, name='profile')
]