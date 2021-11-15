from django.shortcuts import render
from principal.models import Bebida

# Create your views here.
def lista_bebidas(request):
    bebidas = Bebida.objects.all()
    return render(request, 'lista_bebidas.html',{'lista':bebidas})
