from telebot import types
from telebot.types import InlineKeyboardMarkup
from services.database import get_page_category, get_quantity_user_tags, get_page_quote, get_quantity_user_quotes_by_tag
import math


def quote_keyboard(quote_id) -> InlineKeyboardMarkup():
    # Это просто inline-клавиатура для работы с конкретной цитатой, возвращает объект клавиатуры
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Удалить из избранного", callback_data=f"fav:del:{quote_id}")
    btn2 = types.InlineKeyboardButton("Поменять категорию", callback_data=f"fav:chng:{quote_id}")
    kb.add(btn1, btn2)
    return kb

def navigation_quotes_categories_menu(user_id, page = 0):
    '''
    Здесь у нас будет менюшка выбора категории цитат, с которой хочет работать пользователь
    Текст сообщения: Выберите категорию, с которой хотели бы работать:
    Далее 4 inline-кнопки форматом 2х2 - названия [n, n+3] категорий в отсортированном списке
    После 2 ряда с НОМЕРАМИ СТРАНИЦ категорий (не с самими категориями)
    Далее 1/2 кнопки Следующая/Предыдущая (в зависимости, есть ли до/после этой страницы со страницами или нет

    Пока отказываюсь от этого функционала, голова кипит
    '''
    kb = types.InlineKeyboardMarkup(row_width = 5)
    limit = 4
    temp_list = get_page_category(user_id = user_id, page = page, limit = limit)
    for Tag, quantity_quotes in temp_list:
        # Делаю коллбэки для всех категорий сразу на нулевую страницу
        kb.add(types.InlineKeyboardButton(text=f"{Tag} - Кол-во цитат: {quantity_quotes}", callback_data=f"nav:cat:tag:{Tag}:0"))

    quantity_pages = math.ceil(get_quantity_user_tags(user_id)/limit)
    print(get_quantity_user_tags(user_id))
    kb.add(*[types.InlineKeyboardButton(text=f"{btn}", callback_data=f"nav:cat:{btn}") for btn in range(quantity_pages) if btn != page])

    # if page != 0:
    #     kb.add(types.InlineKeyboardButton(text=f"Предыдущая страница", callback_data=f"nav:cat:{page-1}"))
    # if page != quantity_pages:
    #     kb.add(types.InlineKeyboardButton(text=f"Следующая страница", callback_data=f"nav:cat:{page+1}"))

    return kb

def navigation_quotes_in_cat_menu(user_id, Tag, page = 0):
    '''
    Короче, я на верном пути, однако в качестве улучшения на будущее можно не передавать целые огромные массивы
    в функцию клавиатуры, а лишь вытаскивать нужную для показа часть.
    Здесь возникает вопрос: либо мне важнее скорость вычислений (тогда я через условие SQL
    ограничиваю нужный мне вывод и часто обращаюсь к бд), либо мне важнее ограничить кол-во обращений к бд (выгружаю полностью)
    '''
    kb = types.InlineKeyboardMarkup(row_width=5)
    limit = 3
    temp_list = get_page_quote(user_id=user_id, tag= Tag, page=page, limit=limit)
    for Quote, id in temp_list:
        # Делаю коллбэки для всех цитат, передавай id записи
        kb.add(types.InlineKeyboardButton(text=f"{Quote}", callback_data=f"nav:cat:tag:{Tag}:quote:{id}"))

    quantity_pages = math.ceil(get_quantity_user_quotes_by_tag(user_id=user_id, Tag=Tag) / limit)
    kb.add(
        *[types.InlineKeyboardButton(text=f"{btn}", callback_data=f"nav:cat:tag:{Tag}:{btn}") for btn in range(quantity_pages) if
          btn != page])

    # if page != 0:
    #     kb.add(types.InlineKeyboardButton(text=f"Предыдущая страница", callback_data=f"nav:cat:tag:{Tag}:{page-1}"))
    # if page != quantity_pages:
    #     kb.add(types.InlineKeyboardButton(text=f"Следующая страница", callback_data=f"nav:cat:tag:{Tag}:{page+1}"))

    return kb