from whoosh.fields import Schema, TEXT, DATETIME
from whoosh.index import create_in
import os
import shutil
from datetime import datetime

INDEXDIR = 'Ejercicio 10/indexdir'

def save() -> None:
    '''Indexa los correos con los siguientes atributos: 
    remitente, destinatarios, fecha, asunto y cuerpo del texto'''
    schema = Schema(remitente=TEXT(stored=True), destinatarios=TEXT(stored=True), fecha=DATETIME, asunto=TEXT(stored=True)
    , cuerpo=TEXT, fichero=TEXT(stored=True))

    if os.path.exists(INDEXDIR):
        shutil.rmtree(INDEXDIR)
    os.mkdir(INDEXDIR)
    ix = create_in(INDEXDIR, schema)
    writer = ix.writer()

    path = 'Ejercicio 10/Correos/'
    for correo in os.listdir(path):
        add_correo(f'{path}{correo}', writer)
    
    writer.commit()

def add_correo(path: str, writer) -> None:
    with open(path, 'r', encoding='utf-8') as f:
        correo_str = f.read().split('\n')
        writer.add_document(remitente=correo_str[0], destinatarios=correo_str[1], fecha=datetime.strptime(correo_str[2].strip(), '%Y%m%d'), 
                            asunto=correo_str[3], cuerpo='\n'.join(correo_str[4:]), fichero=path)

def get_agenda() -> dict[str, str]:
    agenda = dict()
    with open('Ejercicio 10/Agenda/agenda.txt', 'r', encoding='utf-8') as f:
        lineas = f.read().split('\n')
        for i in range(int(len(lineas)/2)):
            agenda[lineas[2*i]] = lineas[2*i + 1]
    return agenda

if __name__ == '__main__':
    save()
    print(get_agenda())