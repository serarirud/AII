from django.contrib import admin
from principal.models import Temporada, Jornada, Equipo, Partido

# Register your models here.
admin.site.register(Temporada)
admin.site.register(Jornada)
admin.site.register(Equipo)
admin.site.register(Partido)