# Так-с, по-тихоньку начнем ставить нужный функционал с кнопками и API запросами
# Пока сделает монолитную структуру, потом введем разделение по пользователям и разделим на отдельные файлы
import telebot
import private_info as pin
from handlers.base import register_base_handlers
from handlers.quotes import register_bot_handlers
from handlers.callbacks import register_callback_handlers

bot = telebot.TeleBot(pin.TOKEN, parse_mode = None)
register_base_handlers(bot)
register_bot_handlers(bot)
register_callback_handlers(bot)


if __name__ == "__main__":
    try:
        bot.infinity_polling()
    finally:
        from services.database import conn #импортируем объект соединения, т.к. он был создан в другом файле
        conn.close() #И закрываем его