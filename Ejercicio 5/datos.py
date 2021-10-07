import sqlite3
import urllib
from urllib import request
from bs4 import BeautifulSoup

DATABASE = 'database.db'
LINK = 'https://www.elseptimoarte.net/estrenos/'

def get_data() -> list[tuple[str, str, str, str, str, str]]:
    '''Accede a la web y obtiene los siguientes datos de los
    estrenos en España: Título, Título original, País/es, Fecha de
    estreno en España, Director y Género/s'''
    
    raw_html = urllib.request.urlopen(LINK).read().decode('ISO-8859-1')
    html = BeautifulSoup(raw_html, 'html.parser')
    datos = []
    for li in html.find_all(class_='elements')[0].find_all('li'):
        url = LINK.replace('/estrenos/', '') + li.h3.a['href']
        datos.append(get_film_data_from_url(url))
    return datos

def get_film_data_from_url(url: str) -> tuple[str, str, str, str, str, str]:
    raw_html = urllib.request.urlopen(url).read().decode('ISO-8859-1')
    html = BeautifulSoup(raw_html, 'html.parser')
    
    generos: str = ', '.join([element.contents[0] for element in html.find_all(class_='categorias')[0].find_all('a')])
    dts = html.find_all('dt')
    datos = dict()
    for dt in dts:
        datos[dt.contents[0]] = dt.next_sibling.next_sibling
    
    titulo = datos['Título'].contents[0]
    titulo_original = datos['Título original'].contents[0]
    paises = ', '.join([element.contents[0] for element in datos['País'].find_all('a')])
    fecha_estreno = datos['Estreno en España'].contents[0].replace('/', '-')
    director = ', '.join([element.contents[0] for element in datos['Director'].find_all('a')])

    return titulo, titulo_original, paises, fecha_estreno, director, generos

def save_data() -> int:
    con = sqlite3.connect(DATABASE)
    con.execute('DROP TABLE IF EXISTS Films')
    con.execute('''CREATE TABLE IF NOT EXISTS Films (
        Titulo varchar(255),
        Titulo_original varchar(255),
        Pais varchar(255),
        Fecha varchar(255),
        Director varchar(255),
        Generos varchar(255)
    )''')
    film_data = get_data()
    for element in film_data:
        con.execute('''INSERT INTO Films (Titulo, Titulo_original, Pais, Fecha, Director, Generos) VALUES 
                        (?, ?, ?, ?, ?, ?)''', element)
    con.commit()
    con.close()

    con = sqlite3.connect(DATABASE)
    size = con.execute('SELECT Count(*) FROM Films').fetchall()[0][0]
    con.close()
    return size

def find_all() -> list[tuple[str, str, str, str, str, str]]:
    con = sqlite3.connect(DATABASE)
    data = con.execute('SELECT * FROM Films').fetchall()
    con.close()
    return data

if __name__ == '__main__':
    print(get_film_data_from_url('https://www.elseptimoarte.net/peliculas/titane-23427.html'))
    # print(get_data())
    save_data()
    con = sqlite3.connect(DATABASE)
    print(con.execute('SELECT Count(*) FROM Films').fetchall()[0][0])
    con.close()