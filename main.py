import os
from flask import Flask
from threading import Thread
import telebot

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

TOKEN = "8967353300:AAE97mcx7MtDSiWDpiTDDjNbduNlXGiHjZs"
bot = telebot.TeleBot(TOKEN)

user_state = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_state[chat_id] = "waiting_for_device"
    bot.reply_to(message, "Bolo, kaun se device ki paid sensi chahiye?\n(Jaise: Poco, Vivo, Oppo, Realme, Redmi)")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()
    state = user_state.get(chat_id)

    if state == "waiting_for_device":
        user_state[chat_id] = "waiting_for_payment"
        bot.reply_to(message, f"Acha, {text} device ki paid sensi ka price **Rs. 50** hai.\n\nNeeche diye gaye UPI ID par payment karo aur uska screenshot yahin bhejo:\n\nUPI ID: `example@upi`")

    elif state == "waiting_for_payment":
        if message.photo:
            bot.reply_to(message, "Payment screenshot mil gaya hai! ✅\nAdmin verify kar raha hai, jaldi hi aapko sensi mil jayegi.")
        else:
            bot.reply_to(message, "Bhai, please payment karne ke baad uska screenshot upload karo.")
    else:
        bot.reply_to(message, "Dobara shuru karne ke liye /start dabayein.")

bot.infinity_polling()
