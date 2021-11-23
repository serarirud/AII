from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Ocupacion(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    genero = models.CharField(max_length=1, primary_key=True)

    def __str__(self):
        return self.genero

class Usuario(models.Model):
    edad = models.IntegerField(validators=[MinValueValidator(0)])
    sexo = models.ForeignKey(Genero, on_delete=models.CASCADE)
    ocupacion = models.ForeignKey(Ocupacion, on_delete=models.CASCADE)
    codigo_postal = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.edad} {self.sexo} {self.ocupacion} {self.codigo_postal}'

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Pelicula(models.Model):
    titulo = models.CharField(max_length=100)
    fecha_estreno = models.DateTimeField()
    imdb_url = models.URLField()
    categorias = models.ManyToManyField(Categoria)

    def __str__(self):
        return f'{self.titulo} {self.fecha_estreno} {self.imdb_url} {self.categorias}'

class Puntuacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)

