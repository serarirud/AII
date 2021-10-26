import whoosh
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in
from bs4 import BeautifulSoup
from tkinter import messagebox
import urllib
import urllib.request
import datetime
import os
import shutil
import re

INDEXDIR = 'Ejercicio 9/indexdir'
LINK = 'https://www.meneame.net/?page={}'

def cargar() -> None:
    '''Guarda el título, autor, fuente de la noticia y enlace de la noticia, fecha y contenido.'''
    schema = Schema(titulo=TEXT(stored=True), autor=TEXT(stored=True), fuente=TEXT(stored=True), enlace=TEXT(stored=True)
                    , fecha=TEXT, contenido=TEXT)
    
    if os.path.exists(INDEXDIR):
        shutil.rmtree(INDEXDIR)
    os.mkdir(INDEXDIR)
    ix = create_in(INDEXDIR, schema)
    writer = ix.writer()
    n = 0

    for i in range(3):
        raw_html = urllib.request.urlopen(LINK.format(i+1)).read().decode('utf-8')
        html = BeautifulSoup(raw_html, 'html.parser')
        for noticia in html.find_all(class_='news-summary'):
            titulo = noticia.find_all(class_='center-content')[0].h2.a.contents[0]
            autor = noticia.find_all(class_='news-submitted')[0].find_all('a')[1].contents[0]
            try:
                fuente = noticia.find_all(class_='news-submitted')[0].find_all('span')[0].contents[0]
                enlace = noticia.find_all(class_='center-content')[0].h2.a['href']
            except Exception:
                fuente = 'Anónimo'
                enlace = 'Desconocido'
                
            fecha = datetime.datetime.fromtimestamp(
                float(noticia.find_all(class_='news-submitted')[0].find_all('span', title=re.compile('publicado'))[0]['data-ts'])
                )
            contenido = noticia.find_all(class_='news-content')[0].contents[0]
            writer.add_document(titulo=str(titulo), autor=str(autor), fuente=str(fuente), enlace=str(enlace)
                                , fecha=str(fecha), contenido=str(contenido))
            n+=1

    writer.commit()
    messagebox.showinfo('Se han guardado {} noticias'.format(n))


if __name__ == '__main__':
    cargar()

