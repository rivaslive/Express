from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.utils.timezone import now



class TipoMembresia(models.Model):
    tipo = models.CharField(max_length=60, blank=False, null=False)
    descripcion = models.CharField(max_length=200, blank=False, null=False)
    estado = models.BooleanField(default=True, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.tipo)


class Cliente(models.Model):
    genero = models.CharField(max_length=60, blank=False, null=False)
    nombre = models.CharField(max_length=60, blank=False, null=False)
    correo = models.CharField(max_length=60, blank=False, null=False)
    telefono = models.IntegerField(blank=False, null=False)
    modelo = models.CharField(max_length=60, blank=False, null=False)
    color = models.CharField(max_length=60, blank=False, null=False)
    matricula = models.CharField(max_length=20, blank=False, null=False)
    marca = models.CharField(max_length=60, blank=False, null=False)
    anio = models.IntegerField(blank=False, null=False)
    estado = models.BooleanField(default=True, blank=False, null=False)

    def __str__(self):
        return '{} AutoMovil: {} {}'.format(self.nombre, self.marca, self.modelo)


class TipoDeOperacion(models.Model):
    tipo = models.CharField(max_length=60, blank=False, null=False)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    estado = models.BooleanField(default=True, blank=False, null=False)

    def __str__(self):
        return '{} ${}'.format(self.tipo, self.precio)



class Membresia(models.Model):
    cliente = models.ForeignKey(Cliente, blank=False, null=False, on_delete=models.CASCADE)
    tipoMembresia = models.ForeignKey(TipoMembresia, blank=False, null=False, on_delete=models.CASCADE)
    inicioMembresia = models.DateField(default=now(), blank=False, null=False)
    finalMembresia = models.DateField(default=(now() + timedelta(days=30)), blank=False, null=False)
    estado = models.BooleanField(default=True, blank=False, null=False)


class Operacion(models.Model):
    Membresia = models.ForeignKey(Membresia, blank=True, null=True, on_delete=models.CASCADE)
    tipoOperacion = models.ForeignKey(TipoDeOperacion, blank=False, null=False, on_delete=models.CASCADE)
    fechaOperacion = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    observaciones = models.CharField(max_length=200, blank=False, null=False)
    estado = models.BooleanField(default=True, blank=False, null=False)

    def __self__(self):
        return '{} {}'.format(self.Membresia, self.tipoOperacion)


class FacturaOperacion(models.Model):
    operacion = models.OneToOneField(Operacion, null=False, blank=False, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    cambio = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    fecha = models.DateTimeField(default=now, null=False, blank=False)
    numero = models.IntegerField(default=00000000, null=False, blank=False)
    efectivo = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    descuentoTotal = models.DecimalField(default=0, max_digits=5, decimal_places=2, null=True, blank=True)
    estado = models.BooleanField(default=True, blank=False, null=False)
