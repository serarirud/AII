import sqlite3
from bs4 import BeautifulSoup
import urllib

DATABASE = 'database.db'
LINK = 'https://www.vinissimus.com'
PARAMETERS = '/es/vinos/tinto?cursor={}'

def guardar_datos(vinos: list[tuple[str, float, str, str, list[str]]]) -> int:
    '''Crea una tabla para uvas, denominación y vino y guarda los datos'''
    con = sqlite3.connect(DATABASE)
    con.execute('''DROP TABLE IF EXISTS Vinos''')
    con.execute('''DROP TABLE IF EXISTS UvasVino''')
    con.execute('''CREATE TABLE Vinos (
                    ID int UNIQUE,
                    Nombre varchar(255),
                    Precio float,
                    Denominacion varchar(255),
                    Bodega varchar(255),
                    PRIMARY KEY (ID)
                );''')
    con.execute('''CREATE TABLE UvasVino (
                    VinoID int,
                    Uva varchar(255),
                    FOREIGN KEY (VinoID) REFERENCES Vinos(ID)
                );''')
    
    for i, vino in enumerate(vinos):
        con.execute('INSERT INTO Vinos (ID, Nombre, Precio, Denominacion, Bodega) VALUES (?, ?, ?, ?, ?)', (i, vino[0], vino[1], vino[2], vino[3]))
        for uva in vino[4]:
            con.execute('INSERT INTO UvasVino (VinoID, Uva) VALUES (?, ?)', (i, uva))
    
    con.commit()
    num = con.execute('SELECT Count(*) FROM Vinos').fetchall()[0][0]
    con.close()
    return num

def get_vinos() -> list[tuple[str, float, str, str, list[str]]]:
    con = sqlite3.connect(DATABASE)
    vinos = []
    vinos_database = con.execute('SELECT ID, Nombre, Precio, Denominacion, Bodega FROM Vinos').fetchall()
    for vino in vinos_database:
        uvas = [uva[0] for uva in con.execute('SELECT Uva FROM UvasVino WHERE VinoID = ?', (vino[0],)).fetchall()]
        vinos.append((vino[1], vino[2], vino[3], vino[4], uvas))
    
    return vinos

def descargar_datos() -> list[tuple[str, float, str, str, list[str]]]:
    '''Devuelve una lista de tuplas con los siguientes datos:
    nombre, precio, denominación, bodega y tipo de uva'''
    num_vinos = get_numero_de_vinos() # Muchos vinos
    vinos_por_pagina = 24
    vinos = []
    for i in range(0, num_vinos, vinos_por_pagina):
        raw_html = urllib.request.urlopen(LINK + PARAMETERS.format(i))
        html = BeautifulSoup(raw_html, 'html.parser')
        for vino in html.find_all(class_='product-list-item'):
            try:
                enlace = LINK + vino.find_all('div')[0].find_all('div')[2].a['href']
                print(i, enlace)
                vinos.append(descargar_datos_vino(enlace))
            except:
                enlace = LINK + vino.find_all('div')[0].find_all('div')[3].a['href']
                print(i, enlace)
                vinos.append(descargar_datos_vino(enlace))

    return vinos

def descargar_datos_vino(url) -> tuple[str, float, str, str, list[str]]:
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
    # guardar_datos(vinos)
    # get_vinos()

    # descargar_datos_vino('https://www.vinissimus.com/es/vino/abadia-retuerta-seleccion-especial/')
    # descargar_datos_vino('https://www.vinissimus.com/es/vino/pago-de-carraovejas/')