from telebot import types
from services.quotes_api import fetch_random_quote_ru
from services.database import add_favourite_quote, get_random_fav, get_actual_user_tags
from services.cats_api import fetch_random_catfact_ru
from services.keyboards import quote_keyboard, navigation_quotes_categories_menu
import math


def register_bot_handlers(bot):
    @bot.message_handler(func = lambda message: message.text == "Случайная цитата")
    def send_quote(message):
        text, author = fetch_random_quote_ru()
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("Добавить в избранное", callback_data="fav:add"))
        bot.send_message(chat_id=message.chat.id, text=f"{text}\n - {author}", reply_markup=kb)

    @bot.message_handler(func = lambda m:m.text == "Случайная избранная")
    def random_fav(message):
        user_id=message.from_user.id
        res = get_random_fav(user_id)
        if not res:
            bot.send_message(chat_id=message.chat.id, text = "Цитат у Вас нет!")
            return

        quote_id, text, tag = res
        kb = quote_keyboard(quote_id)
        bot.send_message(chat_id=message.chat.id, text=f"{text}\nКатегория: {tag}", reply_markup=kb)










    @bot.message_handler(func = lambda m:m.text == "Навигация по своим цитатам")
    def nav_quotes(message):
        kb = navigation_quotes_categories_menu(user_id=message.from_user.id, page=0)
        bot.send_message(chat_id=message.chat.id, text=f"Выберите желаемую категорию:", reply_markup=kb)







    @bot.message_handler(func=lambda m:m.text == "Работа с категориями")
    def edit_tags(message):
        kb = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Добавить категорию", callback_data = "tag:add")
        item2 = types.InlineKeyboardButton("Удалить категорию", callback_data = "tag:del")
        kb.add(item1, item2)
        temp_list = get_actual_user_tags(message.from_user.id)
        text = "\n".join(temp_list)
        bot.send_message(chat_id = message.chat.id, text = f"Это Ваши категории:\n{text}", reply_markup = kb)


    @bot.message_handler(func=lambda m: m.text == "Случайный факт о котах")
    def send_fact(message):
        bot.send_message(chat_id=message.chat.id, text = fetch_random_catfact_ru())




