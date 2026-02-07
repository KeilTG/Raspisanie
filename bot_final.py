import telebot
import json
import time
import schedule
import threading

bot = telebot.TeleBot("8288669449:AAGGeY4yI8SnRCkOmWOlFQ-Yq43n8x-uPWg")

#добавляем группы
try:
    with open('groups.json') as f:
        groups = json.load(f)
except:
    groups = {"1ip6": [], "1vr1": []}

def save():
    with open('groups.json', 'w') as f:
        json.dump(groups, f)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Напишите свою группу! \nПример: 1ip6 , 1vr1 , 1rki2 .")

@bot.message_handler(func=lambda m: m.text in ["1ip6", "1vr1"])
def add(message):
    g = message.text
    uid = message.from_user.id
    
    if g not in groups:
        groups[g] = []
    
    if uid not in groups[g]:
        groups[g].append(uid)
        save()
        bot.reply_to(message, f" В {g}")
    else:
        bot.reply_to(message, "Уже в группе...")

# Рассылка
def send_all():
    msgs = {"1ip6": "Сообщение 1ip6", "1vr1": "Сообщение 1vr1"}
    for g, users in groups.items():
        for uid in users:
            try:
                bot.send_message(uid, msgs.get(g, "Сообщение"))
            except:
                pass

# Планировщик
def scheduler():
    schedule.every().day.at("00:39").do(send_all) #Тестил
    while True:
        schedule.run_pending()
        time.sleep(1)

# Запуск
threading.Thread(target=scheduler, daemon=True).start()
print("Бот запущен!")
bot.polling(none_stop=True, interval=0, timeout=3)