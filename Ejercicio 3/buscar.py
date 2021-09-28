import sqlite3

def search(query: str, data: tuple) -> list[tuple]:
    if query is None:
        raise Exception()
    
    con = sqlite3.connect('books.db')
    cursor = con.execute(query, data)
    data = list(cursor)
    con.close()
    return data

def search_by_title(title):
    return search('SELECT ISBN, Title, Author, Year FROM Books WHERE Title LIKE ?', ('%{}%'.format(title),))

def get_all_publisher() -> list[str]:
    con = sqlite3.connect('books.db')
    cursor = con.execute('SELECT Publisher FROM Books')
    publishers = list(cursor)
    con.close()
    return publishers

print(search_by_title('Lord of'))