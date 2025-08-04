import sqlite3
import private_info as pin
import atexit
import threading


conn = sqlite3.connect(pin.PATH, check_same_thread=False)
cursor = conn.cursor()
atexit.register(conn.close) #Здесь мы говорим о том, что когда программа завершится, то соединение прекратится в любом случае

_db_lock = threading.Lock()

def add_favourite_quote(user_id: int, Quote: str, Tag: str):
    with _db_lock:
        cursor.execute('INSERT INTO favourite_quotes (user_id, Quote, Tag) VALUES (?, ?, ?)',
                       (user_id, Quote, Tag)
                       )
        conn.commit()

def get_random_fav(user_id):
    with _db_lock:
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
    with _db_lock:
        cursor.execute('''
                DELETE FROM favourite_quotes
                WHERE id = ?
                ''', (id_quote,))
        conn.commit()

def change_tag_by_id(id_quote, Tag):
    with _db_lock:
        cursor.execute('''
            UPDATE favourite_quotes
            SET Tag = ?
            WHERE id = ?
        ''', (Tag, id_quote))
        conn.commit()

def set_new_user(user_id):
    with _db_lock:
        cursor.execute('''
        INSERT INTO user_tags (user_id, Tag)
        SELECT ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM user_tags
            WHERE user_id = ? AND Tag = ?
        ) 
        ''', (user_id, "Без категории", user_id, "Без категории"))
        conn.commit()

def get_actual_user_tags(user_id): #Только те категории цитат, которые актуальны для данного пользователя
    with _db_lock:
        cursor.execute('''
        SELECT * FROM user_tags
        WHERE user_id = ?
        ''', (user_id,))

        temp_list = cursor.fetchall()
        if temp_list:
            temp_tags = []
            for item in temp_list: #Перебираем кортежи
                temp_tags.append(item[2])
            return temp_tags
        else:
            return None

def add_user_tag(user_id, Tag):
    with _db_lock:
        cursor.execute('''
        INSERT INTO user_tags (user_id, Tag)
        SELECT ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM user_tags
            WHERE user_id = ? AND Tag = ?
        )
        ''', (user_id, Tag, user_id, Tag))
        conn.commit()


def del_user_tag(user_id, Tag):
    with _db_lock:
        try:
            cursor.execute('''
            DELETE FROM user_tags
            WHERE user_id = ? AND Tag = ?
            ''', (user_id, Tag))
            conn.commit()
        except:
            conn.rollback()
            raise

def get_page_category(user_id, page, limit): #Здесь будем вытаскивать нужную страницу категорий из бд с кол-вом цитат внутри
    with _db_lock:
        offset = page * limit #Сколько надо пропустить
        try:
            cursor.execute('''
            SELECT Tag, COUNT(*) FROM favourite_quotes
            WHERE user_id = ?
            GROUP BY Tag
            ORDER BY Tag
            LIMIT ? OFFSET ?
            ''', (user_id, limit, offset))
            return cursor.fetchall()
        except:
            return None

def get_quantity_user_tags(user_id):
    with _db_lock:
        try:
            cursor.execute('''
            SELECT COUNT(DISTINCT Tag) FROM favourite_quotes
            WHERE user_id = ?
            ''', (user_id,))
            return int(cursor.fetchone()[0])
        except:
            return None

def get_page_quote(user_id, tag, page, limit): #Здесь будем вытаскивать нужную страницу категорий из бд с кол-вом цитат внутри
    with _db_lock:
        offset = page * limit #Сколько надо пропустить
        try:
            cursor.execute('''
            SELECT Quote, id FROM favourite_quotes
            WHERE user_id = ? AND Tag = ?
            LIMIT ? OFFSET ?
            ''', (user_id, tag, limit, offset))
            return cursor.fetchall()
        except:
            return None

def get_quantity_user_quotes_by_tag(user_id, Tag):
    with _db_lock:
        try:
            cursor.execute('''
            SELECT COUNT(*) FROM favourite_quotes
            WHERE user_id = ? AND Tag = ?
            ''', (user_id, Tag))
            return int(cursor.fetchone()[0])
        except:
            return None

def get_quote_by_id(quote_id):
    with _db_lock:
        try:
            cursor.execute('''
            SELECT Quote FROM favourite_quotes
            WHERE id = ?
            ''', (quote_id,))
            return cursor.fetchone()[0]
        except:
            return None