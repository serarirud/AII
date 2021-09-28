import sqlite3
import csv

BOOKS_FILE_NAME = 'books.{}'

def create_table() -> None:
    con = sqlite3.connect(BOOKS_FILE_NAME.format('db'))
    con.execute('''CREATE TABLE IF NOT EXISTS Books (ISBN int NOT NULL, Title varchar(255) NOT NULL, Author varchar(255), Year int, 
                    Publisher varchar(255), PRIMARY KEY (ISBN))''')
    con.commit()

def import_data_to_db() -> None:
    con = sqlite3.connect(BOOKS_FILE_NAME.format('db'))
    with open(BOOKS_FILE_NAME.format('csv'), 'r', encoding='utf-8') as f:
        lines = csv.reader(f, delimiter=';')
        next(lines)
        for line in lines:
            con.execute('INSERT INTO Books (ISBN, Title, Author, Year, Publisher) VALUES (?,?,?,?,?)',
            (line[0], line[1], line[2], int(line[3]) if line[3] != 'Unknown' else -1, line[4]))
    con.commit()

con = sqlite3.connect(BOOKS_FILE_NAME.format('db'))
con.execute('DROP TABLE IF EXISTS Books')
create_table()
import_data_to_db()
con = sqlite3.connect(BOOKS_FILE_NAME.format('db'))
cursor = con.execute('SELECT * FROM Books')
print(len(list(cursor)))