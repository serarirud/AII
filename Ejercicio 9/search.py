from whoosh.index import open_dir
from whoosh.qparser import QueryParser

INDEXDIR = 'Ejercicio 9/indexdir'

def buscar(palabra: str, campo='contenido') -> list[tuple[str, str, str]]:
    '''Devuelve una lista con titulo, autor y enlace'''
    if campo != 'contenido' and campo != 'fuente':
        raise ValueError('El valor de campo tiene que ser "contenido" o "fuente"')
    if ' ' in palabra.strip():
        raise ValueError('El campo tiene que tener una sola palabra')

    ix = open_dir(INDEXDIR)
    with ix.searcher() as searcher:
        query = QueryParser(campo, ix.schema).parse(palabra)
        if campo == 'contenido':
            campo = 'enlace'
        results: list[tuple[str, str, str]] = [(hit['titulo'], hit['autor'], hit[campo]) for hit in searcher.search(query)]
    
    return results

def buscar_por_contenido(entry1: str) -> list[tuple[str, str, str]]:
    return buscar(entry1, 'contenido')

def buscar_por_fuente(entry1: str) -> list[tuple[str, str, str]]:
    return buscar(entry1, 'fuente')
