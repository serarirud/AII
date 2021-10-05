import datos
import buscar
import tkinter as tk

def start() -> None:
    main_window = tk.Tk()
    
    menu = tk.Menu(main_window, tearoff=0)

    datos = tk.Menu(menu, tearoff=0)
    datos.add_command(label='Cargar', command=cargar_datos)
    datos.add_command(label='Listar', command=listar_datos)
    datos.add_command(label='Salir', command=lambda: salir_app(main_window))

    menu.add_cascade(label='Datos', menu=datos)

    buscar = tk.Menu(menu, tearoff=0)
    buscar.add_command(label='Titulo', command=buscar_titulo)
    buscar.add_command(label='Fecha', command=buscar_fecha)
    buscar.add_command(label='Genero', command=buscar_genero)

    menu.add_cascade(label='Buscar', menu=buscar)
    
    main_window.config(menu=menu)
    main_window.mainloop()

def cargar_datos() -> None:
    pass

def listar_datos() -> None:
    pass

def salir_app(main_window: tk.Tk) -> None:
    main_window.destroy()

def buscar_titulo() -> None:
    pass

def buscar_fecha() -> None:
    pass

def buscar_genero() -> None:
    pass

start()