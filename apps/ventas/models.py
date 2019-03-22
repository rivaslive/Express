from django.db import models
from apps.articulos.models import Articulo
from django.utils.timezone import now

# Create your models here.
from apps.clientes.models import Cliente


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, blank=True, null=True, on_delete=models.CASCADE)
    fecha_venta = models.DateField(null=False, blank=False)
    horaVenta= models.TimeField(auto_now_add=True,null=False,blank=False)
    estado = models.IntegerField(null=False, blank=False)
    def __str__(self):
        return '{}'.format(self.fecha_venta)


class VentaCategoria(models.Model):
    nombreCategoria = models.CharField(max_length=60, blank=False, null=False)
    estado = models.IntegerField(null=False, blank=False)
    def __str__(self):
        return '{}'.format(self.nombreCategoria)

class detalle(models.Model):
    cantidad = models.IntegerField(null=False, blank=False)
    precio = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    descuento = models.DecimalField(default=0, max_digits=5, decimal_places=2, null=True, blank=True)
    descuentoPorcentual = models.DecimalField(default=0, max_digits=5, decimal_places=2, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    id_articulo = models.ForeignKey(
        Articulo, on_delete=models.CASCADE, null=False, blank=False)
    id_venta = models.ForeignKey(
        Venta, on_delete=models.CASCADE, null=False, blank=False)
    id_categoria = models.ForeignKey(VentaCategoria, on_delete=models.CASCADE, null=False, blank=False)

class Factura(models.Model):
    venta = models.OneToOneField(Venta, null=False, blank=False, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    cambio = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    fecha = models.DateTimeField(default=now,null=False, blank=False)
    numero = models.IntegerField(default=00000000, null=False, blank=False)
    efectivo = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    descuentoTotal = models.DecimalField(default=0, max_digits=5, decimal_places=2, null=True, blank=True)
