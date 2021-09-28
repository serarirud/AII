from tkinter.constants import END
from load import cargar
from list import completo, ordenado
from buscar import search_by_title, search_by_publisher, get_all_publishers
import tkinter as tk
from tkinter import messagebox

def show_main_window(main_window: tk.Tk =None) -> None:
    if main_window is not None:
        main_window.destroy()

    main_window = tk.Tk()
    create_option_button(main_window, 'Datos', lambda: show_datos_window(main_window))
    create_option_button(main_window, 'Listar', show_listar_window)
    create_option_button(main_window, 'Buscar', show_search_window)
    main_window.mainloop()

def show_datos_window(main_window: tk.Tk) -> None:
    window = tk.Tk()
    create_option_button(window, 'Cargar', cargar_datos)
    create_option_button(window, 'Salir', main_window.destroy)

def cargar_datos() -> None:
    size = cargar()
    messagebox.showinfo('Carga completada', 'Se han cargado {} datos en la base de datos'.format(size))

def show_listar_window() -> None:
    window = tk.Tk()
    create_option_button(window, 'Completo', datos_completo)
    create_option_button(window, 'Ordenado', datos_ordenado)

def datos_completo() -> None:
    data = completo()
    create_listbox_with_scrollbar(data)

def datos_ordenado() -> None:
    window = tk.Tk()
    create_radiobutton(window, 'Ordenar por año', lambda: show_datos_ordenados(window, 'Year'))
    create_radiobutton(window, 'Ordenar por ISBN', lambda: show_datos_ordenados(window, 'ISBN'))

def show_datos_ordenados(window: tk.Tk, order: str) -> None:
    window.destroy()
    data = ordenado(order)
    create_listbox_with_scrollbar(data)

def show_search_window() -> None:
    window = tk.Tk()
    create_option_button(window, 'Título', buscar_titulo)
    create_option_button(window, 'Editorial', buscar_editorial)

def buscar_titulo() -> None:
    window = tk.Tk()
    create_label(window, 'Introduce un título: ')
    input_ = tk.Entry(window)
    input_.pack(side='left')
    create_option_button(window, 'Buscar', lambda: buscar_titulo_aux(input_))
    window.mainloop()

def buscar_titulo_aux(title: tk.Entry) -> None:
    data = search_by_title(title.get())
    create_listbox_with_scrollbar(data)

def buscar_editorial() -> None:
    window = tk.Tk()
    create_label(window, 'Elige una editorial', 'top')
    options = get_all_publishers()
    spinbox = create_spinbox(window, options)
    create_option_button(window, 'Buscar', lambda: buscar_editorial_aux(window, spinbox), 'top')

def buscar_editorial_aux(window: tk.Tk, spinbox: tk.Spinbox) -> None:
    data = search_by_publisher(spinbox.get())
    window.destroy()
    create_listbox_with_scrollbar(data)

def create_option_button(window: tk.Tk, text: str, command, side='left') -> None:
    option = tk.Button(window)
    option['text'] = text
    option['command'] = command
    option.pack(side=side)

def create_listbox_with_scrollbar(data: list[tuple]) -> None:
    window = tk.Tk()
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side='right', fill='both')
    listbox = tk.Listbox(window, yscrollcommand=scrollbar.set, width=200)
    for d in data:
        listbox.insert(END, str(d))

    listbox.pack(side='left', fill='both')
    scrollbar.config(command=listbox.yview)
    window.mainloop()

def create_radiobutton(window: tk.Tk, option_name: str, command) -> None:
    radiobutton = tk.Radiobutton(window)
    radiobutton['text'] = option_name
    radiobutton['command'] = command
    radiobutton.pack(side='top')

def create_label(window: tk.Tk, text: str, side='left') -> None:
    label = tk.Label(window)
    label['text'] = text
    label.pack(side=side)

def create_spinbox(window: tk.Tk, options: list[str]) -> tk.Spinbox:
    spinbox = tk.Spinbox(window)
    for option in options:
        spinbox.insert(END, option)
    
    spinbox.pack(side='top')
    return spinbox

show_main_window()