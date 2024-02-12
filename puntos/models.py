from django.db import models

# Create your models here.
class TipoOracion(models.Model):
    """Tipos de oraciones. Por ejemplo: Rosario, Denario, Ave María, etc."""
    descripcion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="images/")
    puntos = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.descripcion}"

class Seccion(models.Model):
    """Secciones según rango de edades"""
    descripcion = models.CharField(max_length=100)
    puntos_totales = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.descripcion}"

class Entrada(models.Model):
    """Entrada en línea de tiempo asociada a una sección y una oración"""
    fecha = models.DateField()
    tipo_oracion = models.ForeignKey(TipoOracion, on_delete=models.CASCADE)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.fecha} - {self.seccion} - {self.tipo_oracion}"
