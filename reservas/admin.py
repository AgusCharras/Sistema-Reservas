from django.contrib import admin
from .models import Cliente, Encargado, Complejo, Cabania, Reserva, Servicio, ReservaServicio

# Register your models here.

admin.site.register(Cliente)

admin.site.register(Encargado)

admin.site.register(Complejo)

admin.site.register(Cabania)

admin.site.register(Reserva)

admin.site.register(Servicio)

admin.site.register(ReservaServicio)