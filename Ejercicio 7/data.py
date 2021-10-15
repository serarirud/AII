import sqlite3
from bs4 import BeautifulSoup
import urllib

DATABASE = 'database.db'
LINK = 'https://www.vinissimus.com'
PARAMETERS = '/es/vinos/tinto?cursor={}'

def descargar_datos() -> list[tuple[str, int, str, str, list[str]]]:
    '''Devuelve una lista de tuplas con los siguientes datos:
    nombre, precio, denominación, bodega y tipo de uva'''
    num_vinos = get_numero_de_vinos() # Muchos vinos
    vinos_por_pagina = 36
    vinos = []
    for i in range(0, 36*1, vinos_por_pagina):
        raw_html = urllib.request.urlopen(LINK + PARAMETERS.format(i))
        html = BeautifulSoup(raw_html, 'html.parser')
        for vino in html.find_all(class_='product-list-item'):
            enlace = LINK + vino.find_all('div')[0].find_all('div')[2].a['href']
            print(enlace)
            vinos.append(descargar_datos_vino(enlace))

    return vinos

def get_uvas(vinos: list[tuple[str, int, str, str, list[str]]]) -> set[str]:
    tipos_uvas = set()
    for vino in vinos:
        uvas = set(vino[-1])
        for uva in uvas:
            tipos_uvas.add(uva)

    return tipos_uvas

def get_denominacion(vinos: list[tuple[str, int, str, str, list[str]]]) -> set[str]:
    denominaciones = set()
    for vino in vinos:
        denominacion = vino[2]
        denominaciones.add(denominacion)
    
    return denominaciones

def descargar_datos_vino(url) -> tuple[str, int, str, str, list[str]]:
    '''Dada la página de un vino devuelve los siguiente datos del vino:
    nombre, precio, denominación, bodega y tipo de uva'''

    raw_html = urllib.request.urlopen(url)
    html = BeautifulSoup(raw_html, 'html.parser')

    nombre = html.find_all(class_='product-title')[0].h1.contents[0]
    try:
        precio = float(html.find_all(class_='dto large')[0].contents[0].replace(',', '.')) # Descuento
    except:
        precio = float(html.find_all(class_='price uniq large')[0].contents[0].replace(',', '.'))
    
    denominacion = html.find_all(class_='region')[0].find_all('a')[0].contents[0]
    bodega = html.find_all(class_='cellar')[0].a.contents[0]

    uvas = [uva.contents[0] for uva in html.find_all(class_='tags')[0].find_all('a')]

    return nombre, precio, denominacion, bodega, uvas


def get_numero_de_vinos() -> int:
    raw_html = urllib.request.urlopen(LINK + PARAMETERS.format(0)).read().decode('utf-8')
    html = BeautifulSoup(raw_html, 'html.parser')
    return int(html.find_all(class_='total-count')[0].contents[0].split(' ')[0])

if __name__ == '__main__':
    vinos = descargar_datos()
    print(get_uvas(vinos))
    print(get_denominacion(vinos))

    # descargar_datos_vino('https://www.vinissimus.com/es/vino/abadia-retuerta-seleccion-especial/')
    # descargar_datos_vino('https://www.vinissimus.com/es/vino/pago-de-carraovejas/')