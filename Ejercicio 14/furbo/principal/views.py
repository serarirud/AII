from django.shortcuts import render

# Create your views here.

def get_data() -> dict[str, dict]:
    partido = {'equipo_local': '', 'equipo_visitante': '', 'goles_local': 0, 'goles_visitante': 0, 'jornada': 0}
    equipo = {'nombre': '', 'anyo_fundacion': 0, 'estadio': '', 'aforo': 0, 'direccion': ''}
    jornada =  {'numero': 0, 'fecha': None, 'temporada': ''}
    temporada = {'anyo': 0}

def inicio(request):
    temp = []
    temporadas = {'temporadas': temp, 'size': len(temp)}
    return render(request, 'inicio.html', temporadas)

def ultima_temporada(request):
    # j.partidos_set.all()
    # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_one/
    temporada = {'temporada': '20','jornadas': []}
    return render(request, 'temporada.html', temporada)

def equipos(request):
    equipos = {'equipos': []}
    return render(request, 'equipos.html', equipos)

def equipo(request, id):
    equipo = {'equipo': None}
    return render(request, 'equipo.html', equipo)

def estadios_mayores(request):
    '''Coge los cinco estadios con mayor aforo'''
    estadios = {'estadios': []}
    return render(request, 'estadios.html', estadios)

def cargar(request):
    # hay que borrar todo antes, por cada modelo M, M.objects.all().delete()
    size = {'partidos_size': 0, 'equipo_size': 0, 'jornada_size': 0, 'temporada_size': 0}
    return render(request, 'data_saved.html', size)