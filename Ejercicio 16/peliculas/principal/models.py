from django.db import models

# Create your models here.
class Pais(models.Model):
    nombre = models.CharField(max_length=50)

class Director(models.Model):
    nombre = models.CharField(max_length=50)

class Genero(models.Model):
    nombre = models.CharField(max_length=50)

class Pelicula(models.Model):
    titulo = models.CharField(max_length=50)
    titulo_original = models.CharField(max_length=50)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    generos = models.ManyToManyField(Genero)
