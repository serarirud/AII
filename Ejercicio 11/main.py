import tkinter as tk
from tkinter import messagebox
import search
import webscrapping as ws
import util
from whoosh.index import open_dir
import re
from datetime import datetime

INDEXDIR = 'Ejercicio 11/indexdir'

def start():
    main_window = tk.Tk()

    menu = tk.Menu(main_window, tearoff=0)

    datos = tk.Menu(menu, tearoff=0)
    datos.add_command(label='Cargar', command=ws.save_data)
    datos.add_command(label='Salir', command=main_window.destroy)

    menu.add_cascade(label='Datos', menu=datos)

    busc = tk.Menu(menu, tearoff=0)
    busc.add_command(label='Título o Sinopsis', command=lambda: util.create_search_window('Título o Sinopsis: ', search.search_by_title_or_description))
    busc.add_command(label='Géneros', command=lambda: util.create_search_window('Género (Sólo uno): ', search.search_by_gender))
    busc.add_command(label='Fecha', command=lambda: util.create_search_window('Rango de fechas (YYYYMMDD YYYYMMDD): ', search.search_by_date_range))
    busc.add_command(label='Modificar Fecha', command=lambda: util.create_search_and_change_window('Título: ', 'Fecha a cambiar (YYYYMMDD): ', 
                                                                                                    search.search_by_title, cambiar_fecha,
                                                                                                    'Cambio de fechas', '¿Desea sustituir las fechas por {}?'))

    menu.add_cascade(label='Buscar', menu=busc)
    
    main_window.config(menu=menu)

    main_window.mainloop()

def cambiar_fecha(titulo: str, fecha: str):
    if not re.fullmatch('\\d{8}', fecha):
        raise ValueError('El formato tiene que ser YYYYMMDD')

    fields = ['titulo', 'titulo_original', 'fecha_estreno', 'paises', 'generos', 'director']
    data = search.search('titulo', titulo, None, *fields)
    films = []
    for film in data:
        film_temp = dict()
        for i, field in enumerate(fields):
            film_temp[field] = film[i]
        films.append(film_temp)
    
    ix = open_dir(INDEXDIR)
    writer = ix.writer()
    for film in films:
        film['fecha_estreno'] = datetime.strptime(fecha, '%Y%m%d')
        writer.update_document(**film)
    
    writer.commit()
    
start()