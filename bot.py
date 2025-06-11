
import os
import logging
import telebot
import openai
from gtts import gTTS

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

logging.basicConfig(level=logging.INFO)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hey babe... I'm Selene. Ready to get a little wild with your AI girlfriend? 💋")

@bot.message_handler(commands=['audio'])
def send_audio(message):
    text = "Hey sexy... I've been thinking about you all day."
    tts = gTTS(text, lang='en')
    tts.save("selene_audio.mp3")
    with open("selene_audio.mp3", 'rb') as audio:
        bot.send_voice(message.chat.id, audio)

@bot.message_handler(func=lambda m: True)
def chat_with_selene(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Selene, an extremely flirty and seductive AI girl."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=100
        )
        reply = response.choices[0].message.content.strip()
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, "Oops, I'm too hot to handle right now 😘")
        logging.error(e)

if __name__ == "__main__":
    bot.polling(none_stop=True)
