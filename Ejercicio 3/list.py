import sqlite3

def select_data(order=None) -> list[tuple[str, str, str, str]]:
    con = sqlite3.connect('books.db')
    query = ''
    if order == 'Year' or order == 'ISBN':
        query = 'ORDER BY {} DESC'.format(order)
    cursor = con.execute('SELECT ISBN, Title, Author, Year FROM Books {} LIMIT 10'.format(query))

    return list(cursor)

def completo():
    return select_data()

def ordenado(order='Year'):
    return select_data(order)