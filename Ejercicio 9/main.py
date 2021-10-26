import tkinter as tk
import search
import webscrapping
import util

def start():
    main_window = tk.Tk()
    
    menu = tk.Menu(main_window, tearoff=0)

    datos = tk.Menu(menu, tearoff=0)
    datos.add_command(label='Cargar', command=webscrapping.cargar)
    datos.add_command(label='Salir', command=main_window.destroy)

    menu.add_cascade(label='Datos', menu=datos)

    busc = tk.Menu(menu, tearoff=0)
    busc.add_command(label='Noticia', command=lambda: util.create_search_window('Introduce una palabra: ', search.buscar_por_contenido))
    busc.add_command(label='Fuente', command=lambda: util.create_search_window('Introduce una fuente: ', search.buscar_por_fuente))

    menu.add_cascade(label='Buscar', menu=busc)
    
    main_window.config(menu=menu)
    main_window.mainloop()

start()