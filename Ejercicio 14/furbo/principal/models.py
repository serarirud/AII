from django.db import models

# Create your models here.
class Temporada(models.Model):
    anyo = models.CharField(max_length=9)

    def __str__(self):
        return str(self.anyo)

class Jornada(models.Model):
    numero = models.IntegerField()
    fecha = models.CharField(max_length=50)
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE)

    def __str__(self):
        return f'Jornada {self.numero} - {self.fecha}.'

class Equipo(models.Model):
    nombre = models.CharField(max_length=50)
    fundacion = models.IntegerField()
    estadio = models.CharField(max_length=50)
    aforo = models.IntegerField()
    direccion = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.nombre}'

class Partido(models.Model):
    local = models.ForeignKey(Equipo, related_name='local', on_delete=models.CASCADE)
    visitante = models.ForeignKey(Equipo, related_name='visitante', on_delete=models.CASCADE)
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE)
    goles_local = models.IntegerField()
    goles_visitante = models.IntegerField()
