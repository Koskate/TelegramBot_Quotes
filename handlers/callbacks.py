from telebot import types
from services.database import (add_favourite_quote, delete_quote_by_id,
                               change_tag_by_id, add_user_tag, get_user_tags, del_user_tag)

def register_callback_handlers(bot):
    @bot.callback_query_handler(func = lambda c: c.data.startswith("fav:"))
    def fav_actions(call):
        parts = call.data.split(":") #[fav, add], [fav, del, quote_id],
                            # [fav, chng, quote_id], [fav, chng, quote_id, tag], [fav, set, tag]
        #Нужно запомнить такую структуру коллбэков, мне нравится
        action = parts[1]

        if action == "add":
            kb=types.InlineKeyboardMarkup(row_width=3)
            tag_list = get_user_tags(call.from_user.id)
            temp_list = []
            for tag in tag_list:
                temp_list.append(types.InlineKeyboardButton(tag, callback_data=f"fav:set:{tag}"))
                # Здесь добавим возможность добавлять новые категории (отдельной кнопкой), удалять хз как
            kb.add(*temp_list)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text,
                                  reply_markup = kb)

        elif action=="set":
            user_id, quote, tag = call.from_user.id, call.message.text, parts[2]
            add_favourite_quote(user_id, quote, tag)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Добавлено!")

        elif action == "del":
            delete_quote_by_id(parts[2], call)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Удалено!")

        elif action == "chng" and len(parts) == 3:
            kb = types.InlineKeyboardMarkup(row_width=3)
            tag_list = get_user_tags(call.from_user.id)
            temp_list = []
            for tag in tag_list:
                temp_list.append(types.InlineKeyboardButton(tag, callback_data=f"fav:chng:{parts[2]}:{tag}"))
                # Здесь добавим возможность добавлять новые категории (отдельной кнопкой), удалять хз как
            kb.add(*temp_list)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = call.message.text,
                                  reply_markup=kb)
        elif action == "chng" and len(parts) == 4:
            change_tag_by_id(int(parts[2]), parts[3])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Категория изменена!")

        bot.answer_callback_query(call.id)#Это сообщение телеграмму, что все ок, сообщение получил, бот работает

    @bot.callback_query_handler(func = lambda c: c.data.startswith("tag:"))
    def tag_actions(call):
        parts = call.data.split(":") #[tag, add], [tag, del], [tag, del, Tag]
        action = parts[1]

        if action == "add":
            msg = bot.send_message(chat_id=call.message.chat.id, text = "Напишите название новой категории")
            bot.register_next_step_handler(msg, process_new_tag)
        elif action == "del" and len(parts) == 2:
            kb = types.InlineKeyboardMarkup(row_width=3)
            tag_list = get_user_tags(call.from_user.id)
            temp_list = []
            for tag in tag_list:
                temp_list.append(types.InlineKeyboardButton(tag, callback_data=f"tag:del:{tag}"))
                # Здесь добавим возможность добавлять новые категории (отдельной кнопкой), удалять хз как
            kb.add(*temp_list)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=call.message.text, reply_markup=kb)
        elif action == "del" and len(parts) == 3:
            if parts[2] != "Без категории":
                del_user_tag(call.from_user.id, parts[2])
                bot.send_message(chat_id = call.message.chat.id, text = f"Категория «{parts[2]}» Удалена ✅")
            else:
                bot.send_message(chat_id=call.message.chat.id, text="Без категории по умолчанию есть "
                                                                    "у всех пользователей, ее нельзя удалить")
        bot.answer_callback_query(call.id)  # Это сообщение телеграмму, что все ок, сообщение получил, бот работает


    def process_new_tag(message):
        Tag = message.text.strip()
        user_id = message.from_user.id
        add_user_tag(user_id, Tag)
        bot.send_message(message.chat.id, f"Категория «{Tag}» добавлена ✅")


