# Так-с, по-тихоньку начнем ставить нужный функционал с кнопками и API запросами
# Пока сделает монолитную структуру, потом введем разделение по пользователям и разделим на отдельные файлы

import telebot
from telebot import types
import requests
import googletrans
from googletrans import Translator
import sqlite3

bot = telebot.TeleBot("7285080271:AAFXw3ZWF9yiFvOW2_4Lphafr_i4kdNzaTk", parse_mode = None)
translator = Translator()
conn = sqlite3.connect('D:/Study_Files/Python_Projects/New_start_TGB_Quotes/db/favourite_quotes.db', check_same_thread=False)
cursor = conn.cursor()

#Блок с массивом тэгов цитат
test_tags = ["Важное", "Любовь", "Деньги", "Люди", "Жизнь", "Успех", "Психология", "Из книг", "Смешные", "Счастье", "Без категории"]


@bot.message_handler(commands = ["start"])
def handler_commands(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Случайная цитата")
    item2 = types.KeyboardButton("Случайная избранная")
    item3 = types.KeyboardButton("Навигация по своим цитатам")
    item4 = types.KeyboardButton("Случайный факт о котах")

    markup.add(item1)
    markup.add(item2, item3)
    markup.add(item4)
    bot.send_message(message.chat.id, "Давай начнем, выбирай", reply_markup=markup)

@bot.message_handler(func = lambda message: message.text == "Случайная цитата")
def handler_message(message):
    try:
        params = {
            'method': "getQuote",
            'format': 'json',
            'lang': 'ru',
        }
        data = requests.post('http://api.forismatic.com/api/1.0/', data=params, verify=False).json()
        author = data["quoteAuthor"] if data["quoteAuthor"] else "Неизвестный автор"
        quote = f"{data['quoteText']} \n\n {author}"

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("Добавить в избранное", callback_data = "add_favourite")
        keyboard.add(btn1)

        bot.send_message(message.chat.id, quote, reply_markup = keyboard)
    except Exception as e:
        error_msg = f"🚫 Ошибка: {str(e)}"
        bot.reply_to(message, error_msg)
        print("Error details:", e)

@bot.message_handler(func = lambda message: message.text == "Случайная избранная")
def random_fav_quote(message):
    user_id = message.from_user.id
    id_quote, quote, tag = get_random_fav(user_id)
    if quote:
        keyboard = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Удалить цитату", callback_data = f"fav_del_quote:{id_quote}")
        btn1 = types.InlineKeyboardButton("Поменять категорию", callback_data = f"fav_chng_tag:{id_quote}")

        keyboard.add(btn)
        keyboard.add(btn1)
        bot.send_message(message.chat.id, f"{quote}\n Категория: {tag}", reply_markup = keyboard)
    else:
        bot.send_message(message.chat.id, "У Вас нет цитат")

@bot.callback_query_handler(func = lambda call: call.data.startswith("fav_"))
def fav_del_chng_quote(call):
    fav_del_chng_quote_arr = call.data.split(":")
    id_quote = int(fav_del_chng_quote_arr[1])
    if "del" in call.data:
        cursor.execute('''
        DELETE FROM favourite_quotes
        WHERE id = ?
        ''', (id_quote,))
        conn.commit()
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Удалено!")
    elif "chng" in call.data:
        if len(fav_del_chng_quote_arr) ==2:
            keyboard = types.InlineKeyboardMarkup()
            for i in range(len(test_tags)):
                btn = types.InlineKeyboardButton(test_tags[i], callback_data=f"fav_chng_tag:{id_quote}:{test_tags[i]}")
                keyboard.add(btn)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keyboard)
        else:
            Tag = fav_del_chng_quote_arr[2]
            cursor.execute('''
                UPDATE favourite_quotes
                SET Tag = ?
                WHERE id = ?
                ''', (Tag, id_quote))
            conn.commit()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Тэг изменен!")

@bot.callback_query_handler(func = lambda call: call.data == "add_favourite")
def add_favourite(call):
    message = call.message
    keyboard = types.InlineKeyboardMarkup(row_width = 3)
    for i in range(len(test_tags)):
        btn = types.InlineKeyboardButton(test_tags[i], callback_data=test_tags[i])
        keyboard.add(btn)
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.id, reply_markup = keyboard)

@bot.callback_query_handler(func = lambda call: call.data in test_tags)
def add_tag(call):
    Quote = call.message.text
    Tag = call.data
    user_id = call.from_user.id

    add_favourite_quote(user_id = user_id, Quote = Quote, Tag = Tag)
    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Добавлено!")

@bot.message_handler(func = lambda message: message.text == "Случайный факт о котах")
def send_fact(message):
    try:
        response = requests.get("https://catfact.ninja/fact")

        ru_fact = translator.translate(response.json()['fact'], dest="ru")
        bot.send_message(message.chat.id, ru_fact.text)
    except Exception as e:
        error_msg = f"Ошибка: {str(e)}"
        bot.reply_to(message.chat.id, error_msg)
        print("Error details:", e)

def add_favourite_quote(user_id: int, Quote: str, Tag: str):
    cursor.execute('INSERT INTO favourite_quotes (user_id, Quote, Tag) VALUES (?, ?, ?)', (user_id, Quote, Tag))
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


if __name__ == "__main__":
    bot.infinity_polling()
    conn.close()