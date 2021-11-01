from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import DateRange
from datetime import datetime, timedelta
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

print(buscar('fecha', '{20101016TO]', 'remitente', 'asunto', 'fichero')) # para buscar por fecha al poner {fecha] te busca las fechas posteriores