from urllib import request
import re
import sqlite3
from sqlite3 import Connection, Cursor
import datetime

class InvalidMonthException(Exception):
    pass

class InvalidDateException(Exception):
    pass

def create_table() -> Connection:
    con = sqlite3.connect('database.db')
    con.execute('CREATE TABLE IF NOT EXISTS Noticias (name varchar(256), link varchar(256), date varchar(256))')
    return con

def insert(connection: Connection, name: str, link: str, date: str) -> None:
    connection.execute('INSERT INTO Noticias (name, link, date) VALUES (?, ?, ?)', (name, link, date))

def insert_group(connection: Connection, data: list[dict[str, str]]) -> None:
    for noticia in data:
        name = noticia['name']
        link = noticia['link']
        date = noticia['date']
        insert(connection, name, link, date)

def almacenar(con: Connection):
    '''Obtiene los datos del enlace y los almacena en la base de datos sin commit'''
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
    
    insert_group(con, elements_parsed)
    print('Datos guardados.')

def get_data(con: Connection) -> Cursor:
    '''Devuelve un cursor con los datos'''
    cursor = con.execute('SELECT * FROM Noticias')
    return cursor

def find_data_by_month(con: Connection, month: str) -> list[dict[str, str]]:
    if not re.fullmatch('A-Za-z{2}', month):
        raise InvalidMonthException()
    cursor = get_data(con)
    return [{'name': name, 'link': link, 'date': date} for name, link, date in cursor if re.fullmatch('[\s\S]*?' + month + '[\s\S]*?', date)]

def find_data_by_date(con: Connection, date: str) -> list[dict[str, str]]:
    pattern = '([0-2]\d|3[01])/(0[1-9]|1[0-3])/(20\d{2})'
    if not re.fullmatch(pattern, date):
        raise InvalidDateException()
    
    cursor = get_data(con)
    day, month, year = re.findall(pattern, date)[0]

    date_parsed = datetime.datetime(int(year), int(month), int(day))
    str_date = date_parsed.strftime('%a, %d %b %Y')

    return [{'name': name, 'link': link, 'date': news_date} for name, link, news_date in cursor if re.fullmatch(str_date + '[\s\S]*', news_date)]


    

con = create_table()
almacenar(con)


