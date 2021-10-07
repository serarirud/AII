from tkinter.constants import END
from bs4 import BeautifulSoup
import sqlite3
import tkinter as tk
from tkinter import messagebox
import urllib
from urllib import request
import util

LINK = 'https://resultados.as.com/resultados/futbol/primera/2017_2018/calendario/'
DATABASE = 'database.db'

def get_resultados() -> dict[str, list[dict[str, str]]]:
    raw_html = urllib.request.urlopen(LINK).read().decode('utf-8')
    parsed_html = BeautifulSoup(raw_html, 'html.parser')
    jornadas = parsed_html.find_all(class_="resultados")
    jor_dict = dict()
    for jornada in jornadas:
        jor_list = []
        jor_dict[str(jornada.h2.a['title'])] = jor_list
        for tr in jornada.div.table.tbody.find_all('tr'):
            partido = dict()
            partido['equipo_1'] = tr.find_all('td')[0].a.span.contents[0]
            partido['equipo_2'] = tr.find_all('td')[2].a.find_all('span')[1].contents[0]
            res = tr.find_all('td')[1].a.contents[0].split(' - ')
            partido['result_1'] = int(res[0])
            partido['result_2'] = int(res[1])
            partido['link'] = tr.find_all('td')[1].a['href']
            jor_list.append(partido)

    return jor_dict
    

def almacenar_resultados() -> None:
    '''Almacena en una base de datos los resultados de todas las jornadas y los link del
    de retransmisión de cada partido'''
    datos: dict[str, list[dict[str, str]]] = get_resultados()
    con = sqlite3.connect(DATABASE)
    con.execute('DROP TABLE IF EXISTS Resultados')
    con.execute('''CREATE TABLE IF NOT EXISTS Resultados (
        Jornada varchar(255) NOT NULL,
        Equipo1 varchar(255) NOT NULL,
        Equipo2 varchar(255) NOT NULL,
        Result1 int NOT NULL,
        Result2 int NOT NULL,
        Link varchar(255) NOT NULL
    )''')
    for jornada, partidos in datos.items():
        for partido in partidos:
            con.execute('''INSERT INTO Resultados (Jornada, Equipo1, Equipo2, Result1, Result2, Link) VALUES (?, ?, ?, ?, ?, ?)'''
            , (jornada, partido['equipo_1'], partido['equipo_2'], partido['result_1'], partido['result_2'], partido['link']))

    con.commit()
    con.close()
    con = sqlite3.connect(DATABASE)
    num_partidos = len(con.execute('SELECT * FROM Resultados').fetchall())
    con.close()
    
    messagebox.showinfo('Info', 'Se han guardados {} partidos correctamente'.format(num_partidos))

def get_partidos() -> list[tuple[str]]:
    con = sqlite3.connect(DATABASE)
    data = con.execute('SELECT * FROM Resultados').fetchall()
    con.close()
    return data

def listar_resultados() -> None:
    data = get_partidos()
    window = tk.Tk()
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side='right', fill='both')
    listbox = tk.Listbox(window, yscrollcommand=scrollbar.set, width=200)
    for d in data:
        listbox.insert(END, str(d))

    listbox.pack(side='left', fill='both')
    scrollbar.config(command=listbox.yview)
    window.mainloop()

def buscar_jornada(query1: str) -> list[tuple]:
    con = sqlite3.connect(DATABASE)
    res = list(con.execute('SELECT Equipo1, Result1, Equipo2, Result2 FROM Resultados WHERE Jornada LIKE ?', ('Jornada {}'.format(query1),)))
    con.close()
    return res

def estadisticas_jornada(query1: str) -> list[tuple]:
    con = sqlite3.connect(DATABASE)
    get_goals = 'SELECT Sum(Result{}) FROM Resultados WHERE Jornada LIKE ?'
    goles_totales = con.execute(get_goals.format(1), ('Jornada {}'.format(query1),)).fetchall()[0][0] + con.execute(get_goals.format(2), ('Jornada {}'.format(query1),)).fetchall()[0][0]
    numeros_empates = con.execute('SELECT Count(*) FROM Resultados WHERE Result1 = Result2 AND Jornada LIKE ?', ('Jornada {}'.format(query1),)).fetchall()[0][0]
    victorias_local = con.execute('SELECT Count(*) FROM Resultados WHERE Result1 > Result2 AND Jornada LIKE ?', ('Jornada {}'.format(query1),)).fetchall()[0][0]
    victorias_visitante = con.execute('SELECT Count(*) FROM Resultados WHERE Result1 < Result2 AND Jornada LIKE ?', ('Jornada {}'.format(query1),)).fetchall()[0][0]
    con.close()
    return ['Goles totales: {}'.format(goles_totales), 'Empates: {}'.format(numeros_empates),
            'Victorias local: {}'.format(victorias_local), 'Victorias visitante: {}'.format(victorias_visitante)]

def buscar_goles(query1, query2, query3):
    print(query1, query2, query3)

def start():
    main_window = tk.Tk()
    menu = tk.Menu(main_window, tearoff=0)

    almacenar = tk.Menu(menu, tearoff=0)
    almacenar.add_command(label='Almacenar', command=almacenar_resultados)

    menu.add_cascade(label='Almacenar', menu=almacenar)

    listar = tk.Menu(menu, tearoff=0)
    listar.add_command(label='Listar', command=listar_resultados)

    menu.add_cascade(label='Listar', menu=listar)

    buscar = tk.Menu(menu, tearoff=0)
    buscar.add_command(label='Buscar Jornada', command=lambda: util.create_search_window('Buscar jornada: ', buscar_jornada))
    buscar.add_command(label='Estadísticas Jornada', command=lambda: util.create_search_window('Buscar jornada: ', estadisticas_jornada))
    buscar.add_command(label='Buscar Goles', command=lambda: util.create_search_window(
                                                ['Jornada: ', 'Equipo local: ', 'Equipo visitante:'], buscar_goles)) 

    menu.add_cascade(label='Buscar', menu=buscar)
    
    main_window.config(menu=menu)
    main_window.mainloop()

start()