import tkinter as tk
import util
import data
import search
from tkinter import messagebox

def cargar() -> None:
    '''Extrae y almacena en una base de datos el nombre, precio, denominación,
    bodega y tipos de uva'''
    vinos = data.descargar_datos()
    num = data.guardar_datos(vinos)
    messagebox.showinfo('Vinos', 'Se han guardado {} vinos correctamente en la base de datos'.format(num))

def listar() -> None:
    '''Muestra en una listbox los datos de los vinos guardados en la base de datos'''
    vinos = data.get_vinos()
    util.crear_listbox_con_scrollbar(vinos)

def salir(main_window: tk.Tk) -> None:
    '''Cierra la aplicación'''
    main_window.destroy()

def filtrar_por_denominacion(entry1: str) -> list[tuple[str, float, str, str]]:
    return search.filtar_por_denominacion(entry1)

def filtrar_por_precio(entry1: str) -> list[tuple[str, float, str, str]]:
    return search.filtrar_por_precio(float(entry1))

def listar_por_denominacion() -> None:
    '''Muestra una ventana con un entry en el que el usuario introduce una denominación
    y se muestra en una listbox con scrollbar todos los vinos con dicha denominación'''

def listar_por_precio() -> None:
    '''Pide al usuario un precio y muestra todos los vinos 
    con un precio inferior al indicado'''

def lisar_por_uvas() -> None:
    '''Muestra un spinbox que permite al usuario seleccionar entre distintos tipos de uvas
    y luego muestra una lista con los vinos que contengan dicho tipo de uva'''
    uvas = [uva[0] for uva in search.get_uvas()]
    util.create_spinbox(uvas, search.filtrar_por_uva)

def start() -> None:
    '''Empieza el programa'''
    main_window = tk.Tk()
    
    menu = tk.Menu(main_window, tearoff=0)

    datos = tk.Menu(menu, tearoff=0)
    datos.add_command(label='Cargar', command=cargar)
    datos.add_command(label='Listar', command=listar)
    datos.add_command(label='Salir', command=lambda: salir(main_window))

    menu.add_cascade(label='Datos', menu=datos)

    busc = tk.Menu(menu, tearoff=0)
    busc.add_command(label='Denominación', command=lambda: util.create_search_window_one_entry('Denominación: ', filtrar_por_denominacion))
    busc.add_command(label='Precio', command=lambda: util.create_search_window_one_entry('Precio: ', filtrar_por_precio))
    busc.add_command(label='Uvas', command=lisar_por_uvas)

    menu.add_cascade(label='Buscar', menu=busc)
    
    main_window.config(menu=menu)
    main_window.mainloop()

start()