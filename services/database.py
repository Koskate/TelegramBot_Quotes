import sqlite3
import private_info as pin
import atexit

conn = sqlite3.connect(pin.PATH, check_same_thread=False)
cursor = conn.cursor()
atexit.register(conn.close) #Здесь мы говорим о том, что когда программа завершится, то соединение прекратится в любом случае

def add_favourite_quote(user_id: int, Quote: str, Tag: str):
    cursor.execute('INSERT INTO favourite_quotes (user_id, Quote, Tag) VALUES (?, ?, ?)',
                   (user_id, Quote, Tag)
                   )
    conn.commit()

def get_random_fav(user_id):
    cursor.execute('''
    SELECT id, Quote, Tag FROM favourite_quotes
    WHERE user_id = ?
    ORDER BY RANDOM()
    LIMIT 1
    ''', (user_id,))

    row = cursor.fetchone() #Либо какое-то кортеж, либо None
    if row:
        id_quote, random_quote, tag = row
        return id_quote, random_quote, tag
    else:
        return None


def delete_quote_by_id(id_quote, call):
    cursor.execute('''
            DELETE FROM favourite_quotes
            WHERE id = ?
            ''', (id_quote,))
    conn.commit()

def change_tag_by_id(id_quote, Tag, call):
    cursor.execute('''
        UPDATE favourite_quotes
        SET Tag = ?
        WHERE id = ?
    ''', (Tag, id_quote))
    conn.commit()
