from telebot import types
from telebot.types import InlineKeyboardMarkup
from services.database import get_quotes_by_tag, get_num_quotes_by_tag


def quote_keyboard(quote_id) -> InlineKeyboardMarkup():
    # Это просто inline-клавиатура для работы с конкретной цитатой, возвращает объект клавиатурыв
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Удалить из избранного", callback_data=f"fav:del:{quote_id}")
    btn2 = types.InlineKeyboardButton("Поменять категорию", callback_data=f"fav:chng:{quote_id}")
    kb.add(btn1, btn2)
    return kb

def navigation_quotes_categories_menu(user_tags, count_pages_categories, page = 0):
    '''
    Здесь у нас будет менюшка выбора категории цитат, с которой хочет работать пользователь
    Текст сообщения: Выберите категорию, с которой хотели бы работать:
    Далее 4 inline-кнопки форматом 2х2 - названия [n, n+3] категорий в отсортированном списке
    После 2 ряда с НОМЕРАМИ СТРАНИЦ категорий (не с самими категориями)
    Далее 1/2 кнопки Следующая/Предыдущая (в зависимости, есть ли до/после этой страницы со страницами или нет

    Пока отказываюсь от этого функционала, голова кипит
    '''
    n = 3 #Количество категорий на страницу
    kb = types.InlineKeyboardMarkup(row_width = 5)
    if page != count_pages_categories: #Если не равно максимальному числу, то значит на этой странице точно есть n категории, спокойно заполняем
        for i, tag in enumerate(user_tags[n*page:n*(page+1)]):
            kb.add(types.InlineKeyboardButton(f"{tag}", callback_data= f"nav:quotes_cat:tag:{tag}")) #Здесь у нас в коллбеке КАТЕГОРИЯ
    else: #Тут вот может не быть n категорий, заполняем, что есть
        for i, tag in enumerate(user_tags[count_pages_categories * page:]):
            kb.add(types.InlineKeyboardButton(f"{tag}", callback_data=f"nav:quotes_cat:tag:{tag}"))

    kb.add(types.InlineKeyboardButton(f"###Ниже страницы навигации###", callback_data=f"no_call"))
    kb.add(*[types.InlineKeyboardButton(text = f"{btn}", callback_data=f"nav:quotes_cat:{count_pages_categories}:{btn}")
                                        for btn in range(count_pages_categories) if btn!=page]) #Да, хвастаюсь, знаю генераторы, здесь btn - это номер страницы
    return kb

def navigation_quotes_in_cat_menu(call, Tag, page = 0):
    '''
    Короче, я на верном пути, однако в качестве улучшения на будущее можно не передавать целые огромные массивы
    в функцию клавиатуры, а лишь вытаскивать нужную для показа часть.
    Здесь возникает вопрос: либо мне важнее скорость вычислений (тогда я через условие SQL
    ограничиваю нужный мне вывод и часто обращаюсь к бд), либо мне важнее ограничить кол-во обращений к бд (выгружаю полностью)
    '''
    n = 4
    user_quotes_by_tag = get_quotes_by_tag(user_id=call.from_user.id, Tag = Tag)
    count_pages_categories_quotes = get_num_quotes_by_tag(user_id=call.from_user.id, Tag = Tag)

    kb = types.InlineKeyboardMarkup(row_width=5)
    if page != count_pages_categories_quotes: #Если не равно максимальному числу, то значит на этой странице точно есть n цитат, спокойно заполняем
        for i, Quote in enumerate(user_quotes_by_tag[n*page:n*(page+1)]):
            kb.add(types.InlineKeyboardButton(f"{Quote}", callback_data= f"nav:quotes_cat:search:{Tag}:{Quote}:{call.from_user.id}")) #Здесь у нас в коллбеке ЦИТАТЫ
    else: #Тут вот может не быть n категорий, заполняем, что есть
        for i, Quote in enumerate(user_quotes_by_tag[count_pages_categories_quotes * page:]):
            kb.add(types.InlineKeyboardButton(f"{Quote}", callback_data=f"nav:quotes_cat:search:{Tag}:{Quote}:{call.from_user.id}"))

    kb.add(types.InlineKeyboardButton(f"###Ниже страницы навигации###", callback_data=f"no_call"))
    kb.add(*[types.InlineKeyboardButton(text = f"{btn}", callback_data=f"nav:quotes_cat:tag:{Tag}:{count_pages_categories_quotes}:{btn}")
                                        for btn in range(count_pages_categories_quotes) if btn!=page]) #Да, хвастаюсь, знаю генераторы, здесь btn - это номер страницы
    return kb#[nav, quotes_cat, tag, NameOfCategory, count_pages_categories_quotes, page],
