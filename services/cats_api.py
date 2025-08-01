import requests
from services.translator import translate_ru

cats_api = "https://catfact.ninja/fact"

def fetch_random_catfact_ru():
    try:
        response = requests.get(cats_api)
        ru_fact = translate_ru(response.json()["fact"])
        return ru_fact
    except Exception as e:
        error_msg = f"Ошибка: {str(e)}"
        print("Error details:", e)
