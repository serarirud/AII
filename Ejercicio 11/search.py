from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import re

from whoosh.qparser.default import MultifieldParser

INDEXDIR = 'Ejercicio 11/indexdir'

def search(fields_to_search, str_query: str, limit: int, return_fields: list) -> list[tuple]:
    ix = open_dir(INDEXDIR)
    with ix.searcher() as searcher:

        results: list[tuple] = list()
        if isinstance(fields_to_search, list):
            query = MultifieldParser(fields_to_search, ix.schema).parse(str_query)
        else:
            query = QueryParser(fields_to_search, ix.schema).parse(str_query)
            
        for hit in searcher.search(query, limit=limit):
            datos = [str(hit[c]) for c in return_fields]
            print(type(datos))
            results.append(tuple(datos))
    
    return results

def search_by_title_or_description(words) -> list[tuple[str, str, str]]:
    return search(['titulo', 'sinopsis'], words.replace(' ', ' OR '), 10, ['titulo', 'titulo_original', 'director'])

def search_by_genre(genero_input: str) -> list[tuple[str, str, str]]:
    ix = open_dir(INDEXDIR)
    all_docs = ix.searcher().documents()
    generos = set()
    for hit in all_docs:
        generos_temp = hit['generos'].split(', ')
        for genero in generos_temp:
            generos.add(genero)
    print(generos)
    ix.close()
    genero_input = genero_input.capitalize()
    if genero_input not in generos:
        raise ValueError('Introduce un género válido.')

    return search('generos', genero_input, 20, ['titulo', 'titulo_original', 'paises'])

def search_by_date_range(date_range) -> list[tuple[str, str]]:
    if not re.fullmatch('\\d{8} \\d{8}', date_range):
        raise ValueError('El rango tiene que tener el formato YYYYMMDD YYYYMMDD')
    start, end = date_range.split(' ')

    try:
        return search('fecha_estreno', '{' + f'{start}TO{end}]', None, ['titulo', 'fecha_estreno'])
    except:
        raise ValueError('Valor de fechas incorrecto')

def search_by_title(title: str) -> list[tuple[str, str]]:
    return search('titulo', title.replace(' ', ' OR '), None, ['titulo', 'fecha_estreno'])

if __name__ == '__main__':
    print(search_by_title_or_description('Eternals'))
    print(search_by_title('Alerta'))
    print(search_by_genre('Thriller'))
    # print(search_by_date_range('20211101 20211120'))