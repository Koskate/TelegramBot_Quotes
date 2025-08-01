from telebot import types
from services.quotes_api import fetch_random_quote_ru
from services.database import add_favourite_quote, get_random_fav

TEST_TAGS = [
    'Важное', 'Любовь', 'Деньги', 'Люди', 'Жизнь',
    'Успех', 'Психология', 'Из книг', 'Смешные',
    'Счастье', 'Без категории'
]

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
        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Удалить из избранного", callback_data=f"fav:del:{quote_id}")
        btn2 = types.InlineKeyboardButton("Поменять категорию", callback_data="fav:chng")
        kb.add(btn1, btn2)
        bot.send_message(chat_id=message.chat.id, text=f"{text}\nКатегория: {tag}", reply_markup=kb)


