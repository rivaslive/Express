from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre_Categoria = models.CharField(max_length=45, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.nombre_Categoria)
class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=60, null=False, blank=False)
    telefono = models.CharField(max_length=20, null=False, blank=False)
    marcas= models.CharField(max_length=500, null=False, blank=False)
    correo = models.CharField(max_length=40, null=False, blank=False)
    direccion = models.CharField(max_length=500, null=False, blank=False)
    def __str__(self):
        return '{}'.format(self.nombre_proveedor)


class Articulo(models.Model):
    nombre_articulo = models.CharField(max_length=60, null=False, blank=False)
    codigo_articulo = models.CharField(max_length=45, null=False, blank=False)
    stock = models.IntegerField(null=True, blank=True)
    precio_compra = models.DecimalField(max_digits=5,decimal_places=2,null=False, blank=False)
    precio_venta = models.DecimalField(max_digits=5,decimal_places=2,null=False, blank=False)
    is_activate = models.IntegerField(null=False, blank=False)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=False, blank=False)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE,null=False, blank=False)


class Historial(models.Model):
    id_articulo = models.ForeignKey()
    transaccion=models.CharField(max_length=60, null=False, blank=False) #Esto es por si es entrada o salida
    fecha_venta = models.DateField(null=False, blank=False)
    horaVenta = models.TimeField(auto_now_add=True, null=False, blank=False)
"""
    def __str__(self):
        return '{} {}'.format(self.nombre_articulo, self.codigo_articulo, float(self.precio_unidad))
"""