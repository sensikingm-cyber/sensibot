from flask import Flask
from threading import Thread

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
import os
import telebot

TOKEN = "8967353300:AAGM3Zqzcw5_KmUuvDvZD1saAxkRTw-7fas"
bot = telebot.TeleBot(TOKEN)

user_state = {}

@bot.message_handler(commands=['start'])
def send_welcome(user_message):
    user_state[user_message.chat.id] = "waiting_for_device"
    bot.reply_to(user_message, "Bolo, kaun se device ki paid sensi chahiye?\n(Jaise: Poco, Vivo, Oppo, Realme, Redmi)")

@bot.message_handler(func=lambda m: True)
def handle_message(user_message):
    chat_id = user_message.chat.id
    text = user_message.text.strip()
    state = user_state.get(chat_id)
    
    if state == "waiting_for_device":
        user_state[chat_id] = "waiting_for_payment"
        bot.reply_to(user_message, f"Acha, {text} device ki paid sensi ka price **Rs. 50** hai.\n\nNeeche diye gaye UPI ID par payment karke screenshot yahan bhejo:\n\n**UPI ID:** `yourname@paytm`\n\nPayment ka screenshot bhejne ke baad thoda wait karein.")
    
    elif state == "waiting_for_payment":
        if user_message.photo:
            bot.reply_to(user_message, "Payment screenshot mil gaya hai! ✅\nAdmin verify kar raha hai, jaldi hi aapko sensi file mil jayegi.")
        else:
            bot.reply_to(user_message, "Bhai, please payment karne ke baad uska screenshot upload karo.")
    else:
        bot.reply_to(user_message, "Dobara shuru karne ke liye /start dabayein.")

bot.infinity_polling()

