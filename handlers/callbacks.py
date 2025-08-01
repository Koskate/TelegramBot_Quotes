from telebot import types
from services.database import add_favourite_quote, delete_quote_by_id, change_tag_by_id
from handlers.quotes import TEST_TAGS

def register_callback_handlers(bot):
    @bot.callback_query_handler(func = lambda c: c.data.startswith("fav:"))
    def fav_actions(call):
        parts = call.data.split(":") #[fav, add], [fav, del, quote_id],
                            # [fav, chng, quote_id], [fav, chng, quote_id, tag], [fav, set, tag]
        #Нужно запомнить такую структуру коллбэков, мне нравится
        action = parts[1]

        if action == "add":
            kb=types.InlineKeyboardMarkup(row_width=3)
            temp_list=[]
            for tag in TEST_TAGS:
                temp_list.append(types.InlineKeyboardButton(tag, callback_data=f"fav:set:{tag}"))
                # Здесь добавим возможность добавлять новые категории (отдельной кнопкой), удалять хз как
            kb.add(*temp_list)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text,
                                  reply_markup = kb)

        elif action=="set":
            user_id, quote, tag = call.message.from_user.id, call.message.text, parts[2]
            add_favourite_quote(user_id, quote, tag)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Добавлено!")

        elif action == "del":
            delete_quote_by_id(parts[2], call)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Удалено!")

        elif action == "chng" and len(parts) == 3:
            kb = types.InlineKeyboardMarkup(row_width=3)
            temp_list = []
            for tag in TEST_TAGS:
                temp_list.append(types.InlineKeyboardButton(tag, callback_data=f"fav:set:{tag}"))
                # Здесь добавим возможность добавлять новые категории (отдельной кнопкой), удалять хз как
            kb.add(*temp_list)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text,
                                  reply_markup=kb)
        elif action == "chng" and len(parts) == 4:
            change_tag_by_id(int(parts[2]), parts[3], call)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Категория изменена!")
        bot.answer_callback_query(call.id)#Это сообщение телеграмму, что все ок, сообщение получил, бот работает
