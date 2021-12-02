from django.shortcuts import render
import principal.webscrapping as wb
from principal.models import *

# Create your views here.
def index(request):
    data_len = len(Pelicula.objects.all())
    return render(request, 'index.html', {'size': data_len})

def listar(request):
    return render(request, 'listar_peliculas.html', {'peliculas': Pelicula.objects.all()})

def confirm(request):
    return render(request, 'confirm.html')

def save(request):
    Pelicula.objects.all().delete()
    Director.objects.all().delete()
    Pais.objects.all().delete()
    Genero.objects.all().delete()

    pages = 4
    data = wb.get_data(pages)
    directores = set()
    paises = set()
    generos = set()
    for film in data:
        directores.add(film['director'])
        paises.add(film['pais'])
        for genero in film['generos']:
            generos.add(genero)

    directores = [Director(**{'id': i, 'nombre': n }) for i, n in enumerate(directores)]
    paises = [Pais(**{'id': i, 'nombre': n }) for i, n in enumerate(paises)]
    generos = [Genero(**{'id': i, 'nombre': n }) for i, n in enumerate(generos)]
    Director.objects.bulk_create(directores)
    Pais.objects.bulk_create(paises)
    Genero.objects.bulk_create(generos)

    peliculas = [Pelicula(id=p['id'], titulo=p['titulo'], titulo_original=p['titulo_original'], pais=Pais.objects.filter(nombre=p['pais'])[0]
                , director=Director.objects.filter(nombre=p['director'])[0], fecha=p['fecha']) for p in data]
    Pelicula.objects.bulk_create(peliculas)
    for p in data:
        Pelicula.objects.filter(id=p['id'])[0].generos.set([Genero.objects.filter(nombre=genero)[0] for genero in p['generos']])
    peliculas = len(Pelicula.objects.all())
    paises = len(Pais.objects.all())
    generos = len(Genero.objects.all())
    directores = len(Director.objects.all())
    return render(request, 'save.html', {'peliculas': peliculas, 'paises': paises, 'generos': generos, 'directores': directores})