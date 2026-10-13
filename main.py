import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

BOT_TOKEN = "123456:ABC"  # رح نغيره بعدين بالتوكن تبعك
ADMIN_ID = 0

bot = telebot.TeleBot(BOT_TOKEN)

# قاعدة بيانات بسيطة
conn = sqlite3.connect('store.db', check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS products (name TEXT, price TEXT)")
cur.execute("DELETE FROM products")
cur.execute("INSERT INTO products VALUES ('جنزير', '150 الف'), ('بواجي', '25 الف'), ('دولاب', '200 الف')")
conn.commit()

@bot.message_handler(commands=['start'])
def start(m):
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    markup = InlineKeyboardMarkup(row_width=1)
    for name, price in rows:
        markup.add(InlineKeyboardButton(f"{name} - {price}", callback_data=name))
    bot.send_message(m.chat.id, "🏍️ *متجر الجود لقطع الدراجات*\nاختر القطعة:", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: True)
def buy(c):
    bot.send_message(c.message.chat.id, f"✅ طلبت: {c.data}\nرح نتواصل معك على الواتساب للتوصيل.\nاكتب رقمك وعنوانك:")
    bot.send_message(ADMIN_ID, f"طلب جديد: {c.data} من {c.from_user.first_name} @{c.from_user.username}")

bot.infinity_polling()
