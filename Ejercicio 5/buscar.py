import sqlite3
import re

DATABASE = 'films.db'

class InvalidDateException(Exception):
    pass

def search_by_title(title: str) -> list[tuple[str, str, str]]:
    '''Dado un título devuelve una lista con título, país y director
    que contengan dicho título'''
    con = sqlite3.connect(DATABASE)
    res = list(con.execute('SELECT Titulo, Pais, Director FROM Films WHERE Titulo LIKE ?', ('%{}%'.format(title),)))
    con.close()
    return res

def search_by_date(date: str) -> list[tuple[str, str]]:
    '''Dada una fecha en formate dd-mm-yyyy deuelve una lista
    con los titulos y la fecha de de la fehca introducida'''
    if not re.fullmatch('\d{2}-\d{2}-\d{4}', date):
        raise InvalidDateException
    con = sqlite3.connect(DATABASE)
    res = list(con.execute('SELECT Titulo, Fecha FROM Films WHERE Fecha = ?', (date,)))
    con.close()
    return res

def get_generos() -> list[str]:
    con = sqlite3.connect(DATABASE)
    res_aux = list(con.execute('SELECT Generos FROM Films'))
    res = set()
    for element in res_aux:
        for genero in element[0].split(', '):
            res.add(genero)
    con.close()
    return list(res)

def search_by_gender(gender: str) -> list[tuple[str, str]]:
    '''Dado un género devuelve una lista con titulo y fecha de estreno'''
    con = sqlite3.connect(DATABASE)
    res = list(con.execute('SELECT Titulo, Fecha FROM Films WHERE Generos LIKE ?', ('%{}%'.format(gender),)))
    con.close()
    return res