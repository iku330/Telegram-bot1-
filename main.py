import telebot
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Привет! Напиши /translate и текст — я переведу его на английский!")

@bot.message_handler(commands=['translate'])
def translate(message):
    text = message.text.replace('/translate', '').strip()
    if not text:
        bot.send_message(message.chat.id, "❗ Напиши текст после команды.")
        return

    try:
        response = requests.post(
            'https://libretranslate.com/translate',
            data={
                'q': text,
                'source': 'auto',
                'target': 'en',
                'format': 'text'
            }
        )
        result = response.json()
        translated_text = result['translatedText']
        bot.send_message(message.chat.id, f"🔤 Перевод:\n{translated_text}")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "⚠️ Ошибка перевода")

bot.polling(none_stop=True)
