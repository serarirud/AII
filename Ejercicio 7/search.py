import sqlite3

DATABASE = 'database.db'

def filtar_por_denominacion(denominacion: str) -> list[tuple[str, float, str, str]]:
    con = sqlite3.connect(DATABASE)
    vinos = con.execute('SELECT Nombre, Precio, Bodega, Denominacion FROM Vinos WHERE Denominacion LIKE ?', ('%{}%'.format(denominacion),)).fetchall()
    con.close()
    return vinos

def filtrar_por_precio(precio: float) -> list[tuple[str, float, str, str]]:
    con = sqlite3.connect(DATABASE)
    vinos = con.execute('SELECT Nombre, Precio, Bodega, Denominacion FROM Vinos WHERE Precio < ?', (precio,)).fetchall()
    con.close()
    return vinos

def filtrar_por_uva(uva: str) -> list[tuple[str, str, list[str]]]:
    con = sqlite3.connect(DATABASE)
    vinos = []
    vinos_database = con.execute('''SELECT Vinos.ID, Vinos.Nombre, UvasVino.Uva FROM Vinos INNER JOIN UvasVino ON 
                                Vinos.ID = UvasVino.VinoID AND UvasVino.Uva LIKE ?''', (uva,)).fetchall()
    for vino in vinos_database:
        uvas = [uva[0] for uva in con.execute('SELECT Uva FROM UvasVino WHERE VinoID = ?', (vino[0],)).fetchall()]
        vinos.append((vino[1], uva, uvas))
    con.close()
    return vinos

def get_uvas() -> list[str]:
    con = sqlite3.connect(DATABASE)
    uvas = con.execute('SELECT DISTINCT Uva FROM UvasVino').fetchall()
    con.close()
    return uvas