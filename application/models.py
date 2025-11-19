from django.db import models

class Usuario(models.Model):
    nombre   = models.CharField(max_length=100)
    correo   = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    password = models.CharField(max_length=255)


    def __str__(self):
        return super().nombre
    

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="reservas")
    fecha = models.DateField()
    hora =  models.TimeField()
    actividad = models.CharField(max_length=100)
    notas = models.TextField(blank=True)


    def __str__(self):
        return f"{self.actividad}- {self.fecha} {self.hora}"
    
    
