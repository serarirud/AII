from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import re

INDEXDIR = 'Ejercicio 10/indexdir'

def buscar(campo: str, palabra: str, *campos) -> list[str]:
    ix = open_dir(INDEXDIR)
    with ix.searcher() as searcher:

        results: list[tuple] = list()
        
        query = QueryParser(campo, ix.schema).parse(palabra)
        for hit in searcher.search(query):
            datos = list()
            for c in campos:
                datos.append(hit[c])
            results.append(tuple(datos))
    
    return results

def search_by_subject_or_body(palabra: str) -> list[str, str]:
    res = set()
    res = res.union(set(buscar('asunto', palabra, 'remitente', 'asunto')))
    res = res.union(set(buscar('cuerpo', palabra, 'remitente', 'asunto')))
    return list(res)

def search_by_date(date: str) -> list[str, str, str]:
    if not re.fullmatch('\\d{8}', date):
        raise ValueError('Introduce una fecha con el formato correcto YYYYMMDD')
    
    return buscar('fecha', '{' + f'{date}TO]', 'remitente', 'destinatarios', 'asunto')

if __name__ == '__main__':
    print(buscar('fecha', '{20101016TO]', 'remitente', 'asunto', 'fichero')) # para buscar por fecha al poner {fecha] te busca las fechas posteriores
    print(search_by_subject_or_body('Contrato'))
    print(search_by_date('20101016'))