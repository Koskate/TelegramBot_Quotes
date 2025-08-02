from telebot import types
from services.database import set_new_user

def register_base_handlers(bot): #Я так понимаю, это главная менюшка, откуда будет начинаться взаимодействие пользователя
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Случайная цитата")
        item2 = types.KeyboardButton("Случайная избранная")
        item3 = types.KeyboardButton("Навигация по своим цитатам")
        item5 = types.KeyboardButton("Работа с категориями")
        item4 = types.KeyboardButton("Случайный факт о котах")

        markup.add(item1)
        markup.add(item2, item3)
        markup.add(item5)
        markup.add(item4)
        bot.send_message(message.chat.id, "Давай начнем, выбирай", reply_markup=markup)
        set_new_user(message.from_user.id)