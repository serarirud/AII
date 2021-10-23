import os
import shutil
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser

INDEXDIR = './Ejercicio 8/indexdir'

def save():
    with open('./Ejercicio 8/Correos/1.txt', 'r', encoding='utf-8') as f:
        correo = tuple([linea.strip() for linea in f.readlines()])

    print(correo)

    schema = Schema(remitente=TEXT, destinatarios=TEXT(stored=True))
    if os.path.exists(INDEXDIR):
        shutil.rmtree(INDEXDIR)
    os.mkdir(INDEXDIR)
    ix = create_in(INDEXDIR, schema)

    writer = ix.writer()
    writer.add_document(remitente=correo[0], destinatarios=correo[1])
    writer.commit()

save()

ix = open_dir(INDEXDIR)

with ix.searcher() as searcher:
    query = QueryParser('remitente', ix.schema).parse('unoarrobagmail.com')
    print(searcher.search(query)[0])