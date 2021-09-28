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

def search_by_publisher(publisher):
    return search('SELECT Title, Author, Publisher FROM Books WHERE Publisher LIKE ?', (publisher,))

def get_all_publishers() -> list[str]:
    con = sqlite3.connect('books.db')
    cursor = con.execute('SELECT Publisher FROM Books')
    publishers = {publisher[0] for publisher in cursor}
    con.close()
    return publishers

if __name__ == '__main__':
    print('### Find by title ###')
    print(search_by_title('Lord of'))
    print('### Find by publisher ###')
    print(search_by_publisher('Regan Books'))
    print('### Publishers ###')
    print(get_all_publishers())