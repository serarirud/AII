import urllib
from urllib import request
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import ID, Schema, TEXT, DATETIME
from tkinter import messagebox
import shutil
import os
from datetime import datetime

INDEXDIR = 'Ejercicio 11/indexdir'
LINK = 'https://www.elseptimoarte.net/estrenos/{}/'

def get_data(paginas: int) -> list[dict[str, str]]:
    '''Accede a la web y obtiene los siguientes datos de los
    estrenos en España: Título, Título original, País/es, Fecha de
    estreno en España, Director y Género/s'''
    datos = []
    for i in range(paginas):
        raw_html = urllib.request.urlopen(LINK.format(i+1)).read().decode('ISO-8859-1')
        html = BeautifulSoup(raw_html, 'html.parser')
        for j, li in enumerate(html.find_all(class_='elements')[0].find_all('li')):
            url = 'https://www.elseptimoarte.net' + li.h3.a['href']
            datos.append(get_film_data_from_url(url, j + i*25))
    return datos

def get_film_data_from_url(url: str, id_: int) -> dict[str, str]:
    raw_html = urllib.request.urlopen(url).read().decode('ISO-8859-1')
    html = BeautifulSoup(raw_html, 'html.parser')
    
    generos: str = ', '.join([element.contents[0] for element in html.find_all(class_='categorias')[0].find_all('a')])
    dts = html.find_all('dt')
    datos = dict()
    for dt in dts:
        datos[dt.contents[0]] = dt.next_sibling.next_sibling
    
    try:
        titulo = datos['Título'].contents[0]
    except:
        titulo = datos['Título original'].contents[0]
    titulo_original = datos['Título original'].contents[0]
    paises = ', '.join([element.contents[0] for element in datos['País'].find_all('a')])
    fecha_estreno = datos['Estreno en España'].contents[0].replace('/', '-')
    director = ', '.join([element.contents[0] for element in datos['Director'].find_all('a')])

    return {'id': id_, 'titulo': str(titulo), 'titulo_original': str(titulo_original), 'fecha': datetime.strptime(fecha_estreno, '%d-%m-%Y')
            , 'pais': str(paises).split(', ')[0], 'generos': str(generos).split(', '), 'director': str(director)}

# def save_data() -> None:
#     film_data = get_data()
#     schema = Schema(titulo=TEXT(stored=True), titulo_original=TEXT(stored=True), fecha_estreno=DATETIME(stored=True), paises=TEXT(stored=True)
#                     , generos=TEXT(stored=True), director=TEXT(stored=True), sinopsis=TEXT, url=ID(stored=True, unique=True))
#     if os.path.exists(INDEXDIR):
#         shutil.rmtree(INDEXDIR)
#     os.mkdir(INDEXDIR)
#     index = create_in(INDEXDIR, schema)
#     writer = index.writer()
#     for element in film_data:
#         # print(element['titulo'], element['url'])
#         writer.add_document(**element)
    
#     writer.commit()
    
#     size = len(film_data)
#     messagebox.showinfo('Datos guardados.', f'Se han guardado {size} películas')

if __name__ == '__main__':
    print(get_film_data_from_url('https://www.elseptimoarte.net/peliculas/titane-23427.html', 0))
    # print(get_data())