from tkinter.constants import END
import datos
import buscar
import tkinter as tk
from tkinter import messagebox

def start() -> None:
    main_window = tk.Tk()
    
    menu = tk.Menu(main_window, tearoff=0)

    datos = tk.Menu(menu, tearoff=0)
    datos.add_command(label='Cargar', command=cargar_datos)
    datos.add_command(label='Listar', command=listar_datos)
    datos.add_command(label='Salir', command=lambda: salir_app(main_window))

    menu.add_cascade(label='Datos', menu=datos)

    busc = tk.Menu(menu, tearoff=0)
    busc.add_command(label='Titulo', command=lambda: create_search_window(buscar.search_by_title))
    busc.add_command(label='Fecha', command=lambda: create_search_window(buscar.search_by_date))
    busc.add_command(label='Genero', command=buscar_genero)

    menu.add_cascade(label='Buscar', menu=busc)
    
    main_window.config(menu=menu)
    main_window.mainloop()

def cargar_datos() -> None:
    size = datos.save_data()
    messagebox.showinfo('Datos guardados correctamente', 'Se han almacenado {} películas correctamente'.format(size))

def listar_datos() -> None:
    data = datos.find_all()
    window = tk.Tk()
    crear_listbox_con_scrollbar(window, data)
    window.mainloop()

def crear_listbox_con_scrollbar(data: list[tuple[str, str, str, str, str, str]]) -> None:
    main_window = tk.Tk()
    scrollbar = tk.Scrollbar(main_window)
    scrollbar.pack(side='right', fill='both')
    listbox = tk.Listbox(main_window, yscrollcommand=scrollbar.set, width=200)
    for d in data:
        listbox.insert(END, str(d))
    
    listbox.pack(side='left', fill='both')
    scrollbar.config(command=listbox.yview)
    main_window.mainloop()

def salir_app(main_window: tk.Tk) -> None:
    main_window.destroy()

def create_search_window(command) -> None:
    def listar(event):
        func = lambda search_query: command(search_query)
        data = func(entry.get())
        window.destroy()
        crear_listbox_con_scrollbar(data)
        
    window = tk.Tk()
    entry = tk.Entry(window)
    entry.bind("<Return>", listar)
    entry.pack()
    window.mainloop()

def buscar_genero() -> None:
    pass

start()