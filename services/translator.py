from googletrans import Translator
translator = Translator()

def translate_ru(text):
    return translator.translate(text, dest="ru").text