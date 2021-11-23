from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from principal.models import *
from django.contrib.auth import logout

# Create your views here.
# Mirar CLASE.objects.bulk_create(lista) para añadirlo a la base de datos de una manera más rápida en vez de usar el create

ML = 'ml-100k'

def cargar_ocupacion():
    Ocupacion.objects.all().delete()
    with open(os.path.join(ML, 'u.occupation'), 'r', encoding='utf-8') as f:
        occupations = [Ocupacion(oc.strip() for oc in f.readlines())]
    
    Ocupacion.objects.bulk_create(occupations)

def cargar_categorias():
    Categoria.objects.all().delete()
    with open(os.path.join(ML, 'u.genre'), 'r', encoding='utf-8') as f:
        categorias = [Categoria(int(ca.split('|')[1].strip()), ca.split('|')[0].strip()) for ca in f.readlines() if ca != '\n']
    
    Categoria.objects.bulk_create(categorias)

def cargar_generos():
    Genero.objects.all().delete()
    Genero('M').save()
    Genero('F').save()

def cargar_usuarios() -> dict[int, Usuario]:
    Usuario.objects.all().delete()
    with open(os.path.join(ML, 'u.user'), 'r', encoding='utf8') as f:
        pass

@login_required(login_url='/admin/login/')
def cargar(request):
    cargar_ocupacion()
    cargar_categorias()
    cargar_generos()
    users = cargar_usuarios()
    logout(request)
    return render(request, 'cargar.html', {'size': len(Usuario.objects.all())})

def inicio(request):
    return render(request, 'inicio.html')