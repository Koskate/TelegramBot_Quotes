import requests

forismatic_api = "http://api.forismatic.com/api/1.0/"

def fetch_random_quote_ru() -> tuple[str, str]:
    try:
        params = {
            'method': "getQuote",
            'format': 'json',
            'lang': 'ru',
        }
        data = requests.post(forismatic_api, data=params, verify=False).json()
        author = data.get("quoteAuthor") if data["quoteAuthor"] else "Неизвестный автор"
        text = data.get("quoteText")
        return (text, author)
    except Exception as e:
        error_msg = f"🚫 Ошибка: {str(e)}"
        #bot.reply_to(message, error_msg)
        print("Error details:", e)
        return "Не удалось получить цитату", ""