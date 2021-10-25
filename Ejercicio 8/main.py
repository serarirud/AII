import os
import sqlite3
import shutil
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
import tkinter as tk
import util

INDEXDIR = './Ejercicio 8/indexdir'
DATABASE = 'database.db'

def save():
    schema = Schema(remitente=TEXT, destinatarios=TEXT(stored=True), asunto=TEXT(stored=True), cuerpo=TEXT)

    if os.path.exists(INDEXDIR):
        shutil.rmtree(INDEXDIR)
    os.mkdir(INDEXDIR)
    ix = create_in(INDEXDIR, schema)

    writer = ix.writer()

    con = sqlite3.connect(DATABASE)

    con.execute('DROP TABLE IF EXISTS Remitentes')
    con.execute('''CREATE TABLE Remitentes (
        Remitente varchar(255)
    )''')

    for i in range(6):
        with open('./Ejercicio 8/Correos/{}.txt'.format(i+1), 'r', encoding='utf-8') as f:
            correo_temp = [linea.strip() for linea in f.readlines()]
            correo = (correo_temp[0], correo_temp[1], correo_temp[2], '\n'.join(correo_temp[3:]))

        con.execute('INSERT INTO Remitentes (Remitente) VALUES (?)', (correo[0],))

        writer.add_document(remitente=correo[0], destinatarios=correo[1], asunto=correo[2], cuerpo=correo[3])

    writer.commit()
    con.commit()
    con.close()


def get_remitentes() -> list[str]:
    con = sqlite3.connect(DATABASE)
    res = con.execute('SELECT DISTINCT Remitente FROM Remitentes').fetchall()
    con.close()
    return res

def search(remitente: str) -> list[dict[str, str]]:
    ix = open_dir(INDEXDIR)

    with ix.searcher() as searcher:
        query = QueryParser('remitente', ix.schema).parse(remitente)
        results: list[tuple[str, str]] = [(hit['destinatarios'], hit['asunto']) for hit in searcher.search(query)]
    
    return results
        
def start() -> None:
    main_window = tk.Tk()
    util.create_option_button(main_window, 'Indexar', save)
    util.create_option_button(main_window, 'Buscar remitente', lambda: util.create_spinbox(get_remitentes, search))
    main_window.mainloop()

start()
