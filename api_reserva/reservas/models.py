from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta

# Create your models here.

class Cliente(models.Model):
    dni = models.IntegerField()
    apellido_nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    email = models.CharField(max_length=50, default="user@gmail.com")
    pais = models.CharField(max_length=30, default="Argentina")
    provincia = models.CharField(max_length=30, default="Cordoba")
    localidad = models.CharField(max_length=30, default="Cordoba")

    def __str__(self):
        return self.apellido_nombre

class Encargado(models.Model):
    dni = models.IntegerField()
    apellido_nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    email = models.CharField(max_length=50, default="user@gmail.com")

    def __str__(self):
        return self.apellido_nombre

class Complejo(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    encargado = models.ForeignKey(Encargado, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre


class Cabania(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=15, choices=[('Apart','Apart'), ('Cabaña', 'Cabaña'), ('Departamento','Departamento'), ('Habitacion','Habitacion')])
    capacidad = models.CharField(max_length=2)
    precio = models.FloatField(max_length=10)
    complejo = models.ForeignKey(Complejo, on_delete=models.CASCADE, default="none")

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(default="ninguna", max_length=150)
    precio = models.FloatField(default=0, max_length=20)

    def __str__(self):
        return self.nombre
class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    complejo = models.ForeignKey(Complejo, on_delete=models.CASCADE)
    cabania = models.ForeignKey(Cabania, on_delete=models.CASCADE, default=None)
    diaEntrada = models.DateField()
    diaSalida = models.DateField()
    seña = models.FloatField(default=0, max_length=12)
    precio_original_cabania = models.FloatField(default=0)

    def __str__(self):
        return self.cliente.apellido_nombre
    
    
    def clean(self):
        # Llamamos al método clean de la clase padre para mantener las validaciones predeterminadas
        super().clean()

        # Verificamos si hay reservas existentes con la misma cabaña y fechas superpuestas
        reservas_superpuestas = Reserva.objects.filter(
            cabania=self.cabania,
            diaEntrada__lte =self.diaSalida, 
            diaSalida__gte=self.diaEntrada + timedelta(days=1)
        ).exclude(id=self.id)

        if reservas_superpuestas.exists():
            raise ValidationError('Ya hay una reserva existente para esta cabaña en estas fechas.')
        
        if self.diaEntrada > self.diaSalida:
            raise ValidationError('La fecha de entrada no puede ser posterior a la fecha de salida.')
    

    def save(self, *args, **kwargs):
        # Verificar si el objeto ya existe en la base de datos
        if self.pk is None:
            # Si es una nueva reserva, actualiza el precio original de la cabaña
            self.precio_original_cabania = self.cabania.precio
        super().save(*args, **kwargs)
class ReservaServicio(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    precio_original_servicio = models.FloatField(default=0)  # Campo para almacenar el precio original del servicio en el momento de la reserva

    def __str__(self):
        return f"ReservaServicio {self.id}"

