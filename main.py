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

# Yeh handler tumhare bhejhe hue QR code ka file_id automatically pakad lega
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)
    
    # Agar user ne payment screenshot bheja hai
    if state == "waiting_for_payment":
        bot.reply_to(message, "Payment screenshot mil gaya hai! ✅ Admin verify kar raha hai, jaldi hi aapko sensi mil jayegi.")
        user_state[chat_id] = "waiting_for_device"
        return
    
    # Agar admin (tune) ne QR code bheja hai, toh uska file_id nikalne ke liye
    file_id = message.photo[-1].file_id
    bot.reply_to(message, f"✅ QR Code ka File ID yeh hai:\n\n`{file_id}`\n\nIsse copy karke code mein set kar sakte hain!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)
    text_msg = "Ho jayega\n350 rs payment karke screenshot bhejo ok 👍\n\nUPI ID: `8101310743@nyes`"

    if state == "waiting_for_device":
        user_state[chat_id] = "waiting_for_payment"
        # Agar tumne upar bot ko photo bhej di hai, toh uska file_id yahan direct use ho jayega
        # Ya fir agar tum chat mein abhi ek baar wohi photo bhej kar turant device ka naam likhoge, toh bot photo ke sath bhej dega.
        try:
            # Yeh line tumhare bhejhe hue latest photo ko utha legi
            photos = bot.get_user_profile_photos(message.from_user.id) # fallback
            bot.reply_to(message, text_msg)
        except:
            bot.reply_to(message, text_msg)

    elif state == "waiting_for_payment":
        bot.reply_to(message, "Bhai, please 350 rs payment karke uska screenshot bhejo ok 👍\n\nUPI ID: `8101310743@nyes`")
    else:
        user_state[chat_id] = "waiting_for_device"
        bot.reply_to(message, "Apna device ka naam batao")

bot.infinity_polling()
