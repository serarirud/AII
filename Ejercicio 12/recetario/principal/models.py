from django.db import models

class Bebida(models.Model):
    nombre = models.CharField(max_length=50)
    ingredientes = models.TextField()
    preparacion = models.TextField()

    def __str__(self):
        return self.nombre