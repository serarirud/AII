from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Bebida(models.Model):
    nombre = models.CharField(max_length=25)
    graduacion = models.FloatField(validators=[MinValueValidator(0.), MaxValueValidator(100.)])

    def __str__(self):
        return f'{self.nombre} - {self.graduacion}%'