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
    bot.reply_to(message, "Apna device ka naam batao")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)

    if message.photo:
        bot.reply_to(message, "Payment screenshot mil gaya hai! ✅ Admin verify kar raha hai, jaldi hi aapko sensi mil jayegi.")
        user_state[chat_id] = "waiting_for_device"
        return

    if state == "waiting_for_device":
        user_state[chat_id] = "waiting_for_payment"
        text_msg = "Ho jayega\n350 rs payment karke screenshot bhejo ok 👍\n\nUPI ID: `8101310743@nyes`"
        
        # Yahan humne file ID ki jagah direct chat se uthane wala ya text ke sath bhejane ka code rakha hai
        try:
            # Agar tune bot ko photo bhej rakhi hai, toh uska file_id hum yahan direct hardcode bhi kar sakte hain
            # Par abhi ke liye yeh text aur UPI ID dono bhej raha hai jo bilkul safe hai.
            bot.reply_to(message, text_msg, parse_mode="Markdown")
        except:
            bot.reply_to(message, text_msg)

    elif state == "waiting_for_payment":
        bot.reply_to(message, "Bhai, please 350 rs payment karke uska screenshot bhejo ok 👍\n\nUPI ID: `8101310743@nyes`")
    else:
        user_state[chat_id] = "waiting_for_device"
        bot.reply_to(message, "Apna device ka naam batao")

bot.infinity_polling()
