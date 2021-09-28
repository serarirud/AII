from urllib import request
import re
import sqlite3
from sqlite3 import Connection, Cursor
import datetime
import tkinter as tk
from tkinter.constants import INSERT
from tkinter import messagebox

class InvalidMonthException(Exception):
    pass

class InvalidDateException(Exception):
    pass

class App(tk.Frame):
    con: Connection = None
    
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master=master)
        self.master = master
        self.pack()
        self.create_buttons()
    
    def create_buttons(self):
        self.almacenar_bt = tk.Button(self)
        self.almacenar_bt["text"] = "Almacenar"
        self.almacenar_bt["command"] = self.almacenar
        self.almacenar_bt.pack(side="left")
        self.listar_bt = tk.Button(self)
        self.listar_bt["text"] = "Listar"
        self.listar_bt["command"] = self.listar
        self.listar_bt.pack(side="left")
        self.buscar_mes_bt = tk.Button(self)
        self.buscar_mes_bt["text"] = "Busca mes"
        self.buscar_mes_bt["command"] = self.busca_mes
        self.buscar_mes_bt.pack(side="left")
        self.buscar_dia_bt = tk.Button(self)
        self.buscar_dia_bt["text"] = "Busca dia"
        self.buscar_dia_bt["command"] = self.busca_dia
        self.buscar_dia_bt.pack(side="left")
    
    def create_table(self) -> None:
        self.con = sqlite3.connect('database.db')
        self.con.execute('CREATE TABLE IF NOT EXISTS Noticias (name varchar(256), link varchar(256), date varchar(256))')

    def insert(self, name: str, link: str, date: str) -> None:
        self.con.execute('INSERT INTO Noticias (name, link, date) VALUES (?, ?, ?)', (name, link, date))

    def insert_group(self, data: list[dict[str, str]]) -> None:
        for noticia in data:
            name = noticia['name']
            link = noticia['link']
            date = noticia['date']
            self.insert(name, link, date)

    def almacenar(self):
        '''Obtiene los datos del enlace y los almacena en la base de datos sin commit'''
        self.create_table()
        LINK = 'https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml'

        print('Obteniendo datos de {}'.format(LINK))
        raw = request.urlopen(LINK).read().decode('utf-8')

        regex_pattern = '<item>[\s\S]*?<title>([\s\S]*?)<\/title>[\s\S]*?<link>([\s\S]*?)<\/link>[\s\S]*?<pubDate>([\s\S]*?)<\/pubDate>[\s\S]*?<\/item>'
        parsed = re.findall(regex_pattern, raw)
        elements_parsed = []
        for tup in parsed:
            noticia = dict()
            noticia['name'] = tup[0]
            noticia['link'] = tup[1]
            noticia['date'] = tup[2]
            elements_parsed.append(noticia)
        
        self.insert_group(elements_parsed)
        print('Datos guardados.')
        messagebox.showinfo('Alerta', 'Base de datos creada correctamente')

    def get_data(self) -> Cursor:
        '''Devuelve un cursor con los datos'''
        cursor = self.con.execute('SELECT * FROM Noticias')
        return cursor
    
    def listar(self):
        cursor = self.get_data()
        text = '\n'.join(['{}\n{}\n{}\n'.format(name, link, date) for name, link, date in cursor])
        self.listar_aux(text)
    
    def listar_aux(self, text):
        if len(text) != 0:
            lista_wind = tk.Tk()
            text_widget = tk.Text(lista_wind)
            text_widget.insert(INSERT, text)
            text_widget.pack()
            lista_wind.mainloop()
        else:
            messagebox.showinfo('Alert', 'No se encontraron datos')


    def find_data_by_month(self, month: str) -> list[dict[str, str]]:
        if not re.fullmatch('[A-Z][a-z]{2}', month):
            raise InvalidMonthException()
        cursor = self.get_data()
        return [{'name': name, 'link': link, 'date': date} for name, link, date in cursor if re.fullmatch('[\s\S]*?' + month + '[\s\S]*?', date)]
    
    def busca_mes(self):
        busca_win = tk.Tk()
        label_widget = tk.Label(busca_win)
        label_widget['text'] = 'Introduzca el mes (Xxx)'
        label_widget.pack(side='left')
        month_input = tk.Entry(busca_win)
        month_input.pack(side="left")
        submit = tk.Button(busca_win)
        submit['text'] = 'Buscar'
        submit['command'] = lambda: self.mostrar_filtro(busca_win, month_input)
        submit.pack(side="left")
    
    def mostrar_filtro(self, main_window: tk.Tk, month_input: tk.Entry):
        month = month_input.get()
        main_window.destroy()
        try:
            data = self.find_data_by_month(month)
            text = '\n'.join(['{}\n{}\n{}\n'.format(dicc['name'], dicc['link'], dicc['date']) for dicc in data])
            self.listar_aux(text)
        except InvalidMonthException:
            self.busca_mes()

    def find_data_by_date(self, date: str) -> list[dict[str, str]]:
        pattern = '([0-2]\d|3[01])/(0[1-9]|1[0-3])/(20\d{2})'
        if not re.fullmatch(pattern, date):
            raise InvalidDateException()
        
        cursor = self.get_data()
        day, month, year = re.findall(pattern, date)[0]

        date_parsed = datetime.datetime(int(year), int(month), int(day))
        str_date = date_parsed.strftime('%a, %d %b %Y')

        return [{'name': name, 'link': link, 'date': news_date} for name, link, news_date in cursor if re.fullmatch(str_date + '[\s\S]*', news_date)]
    
    def busca_dia(self):
        busca_win = tk.Tk()
        label_widget = tk.Label(busca_win)
        label_widget['text'] = 'Introduzca el dia (dd/mm/aaaa)'
        label_widget.pack(side='left')
        day_input = tk.Entry(busca_win)
        day_input.pack(side="left")
        submit = tk.Button(busca_win)
        submit['text'] = 'Buscar'
        submit['command'] = lambda: self.mostrar_filtro_dia(busca_win, day_input)
        submit.pack(side="left")
    
    def mostrar_filtro_dia(self, main_window: tk.Tk, day_input: tk.Entry):
        day = day_input.get()
        main_window.destroy()
        try:
            data = self.find_data_by_date(day)
            text = '\n'.join(['{}\n{}\n{}\n'.format(dicc['name'], dicc['link'], dicc['date']) for dicc in data])
            self.listar_aux(text)
        except InvalidDateException:
            self.busca_dia()


root = tk.Tk()
app = App(master=root)
app.mainloop()
# con = create_table()
# almacenar(con)