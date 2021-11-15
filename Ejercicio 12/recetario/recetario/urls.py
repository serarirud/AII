"""recetario URL Configuration


"""
from django.contrib import admin
from django.urls import path
from principal import views

urlpatterns = [
    path('', views.lista_bebidas),
    path('admin/', admin.site.urls),
]
