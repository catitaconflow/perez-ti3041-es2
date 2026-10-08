from django.db import models

class Herramienta(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    marca = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
