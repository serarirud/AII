from dataclasses import dataclass
from urllib import request
import re
import sqlite3
from sqlite3 import Connection

@dataclass
class DatosNoticias():
    name: str
    link: str
    date: str

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

def get_data():
    LINK = 'https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml'

    print('Obteniendo datos de {}'.format(LINK))
    raw = request.urlopen(LINK).read().decode('utf-8')

    regex_pattern = '<item>[\s\S]<title>(.*|[\s\S])<\/title>[\s\S]<link>(.*|[\s\S])<\/link>[\s\S]*<pubDate>(.*|[\s\S])<\/pubDate>[\s\S]*<\/item>'
    parsed = re.findall(regex_pattern, raw)
    print(parsed)
    

get_data()

