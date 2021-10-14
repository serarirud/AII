import sqlite3
from bs4 import BeautifulSoup
import urllib

DATABASE = 'database.db'
LINK = 'https://www.vinissimus.com/es/vinos/tinto/?cursor={}'

def descargar_datos() -> list[tuple[str, int, str, str, str]]:
    '''Devuelve una lista de tuplas con los siguientes datos:
    nombre, precio, denominación, bodega y tipo de uva'''
    num_vinos = get_numero_de_vinos()
    vinos_por_pagina = 36
    for i in range(0, num_vinos, vinos_por_pagina):
        pass
    

def descargar_datos_vino() -> tuple[str, int, str, str, str]:
    '''Dada la página de un vino devuelve los siguiente datos del vino:
    ombre, precio, denominación, bodega y tipo de uva'''

def get_numero_de_vinos() -> int:
    raw_html = urllib.request.urlopen(LINK.format(0)).read().decode('utf-8')
    html = BeautifulSoup(raw_html, 'html.parser')
    return int(html.find_all(class_='total-count')[0].contents[0].split(' ')[0])

if __name__ == '__main__':
    descargar_datos()