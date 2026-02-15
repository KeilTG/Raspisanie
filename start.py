import telebot
import json
import time
import schedule
import threading
from datetime import datetime

bot = telebot.TeleBot("8288669449:AAGGeY4yI8SnRCkOmWOlFQ-Yq43n8x-uPWg")

#добавляем группы
try:
    with open('groups.json', 'r', encoding='utf-8') as f:
        groups = json.load(f)
except:
    groups = {"1ИП-6-25": [], "1ВР-1-25": []}

# добавляем расписание
rasp_path = "rasp.json"
with open(rasp_path, 'r', encoding='utf-8') as f:
    rasp = json.load(f) 

def save():
    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(groups, f, ensure_ascii=False, indent=2)  

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Зачем наш бот???⚡️\n\n✅ Автоматическая рассылка - получайте расписание каждый день в 7:00 утра\n✅ Выбор группы - подпишитесь на свою учебную группу\n✅ Актуальное расписание - всегда свежее расписание на сегодня\n✅ Удобство - получаете расписание без браузеров и сайтов\n✅ Скорость - получение свежей информации в 2 нажатия\n\nКак это все получить?\nПросто напиши свою группу!⭐️\nПример: 1ИП-6-25 , 1ВР-1-25 , 1РКИ-2-25.🤔")

@bot.message_handler(func=lambda m: True)
def add(message):
    g = message.text
    uid = message.from_user.id
    
    # Создаем группу если её нет
    if g not in groups:
        groups[g] = []
    
    # Добавляем пользователя если его нет
    if uid not in groups[g]:
        groups[g].append(uid)
        save()  
        bot.reply_to(message, f"✅ Создана группа {g}, вы добавлены!")
    else:
        bot.reply_to(message, f"⚠️ Уже в группе {g}")

# Рассылка
def send_all():
    """Отправляет каждому пользователю расписание на сегодня"""
    today_num = datetime.now().weekday()
    
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    today_day = days[today_num]
    
    # Для каждой группы отправляем свое расписание
    for group_name, users in groups.items():

        if group_name in rasp and today_day in rasp[group_name]:
            subjects = rasp[group_name][today_day]
            message = f"{group_name}✅\n{today_day}📑\n\n" + "\n".join(subjects)
        else:
            message = f"На {today_day} для {group_name} расписания нет"
        
        # Отправляем каждому пользователю
        for user_id in users:
            try:
                bot.pin_chat_message(user_id, bot.send_message(user_id, message).message_id)
            except:
                pass

# Планировщик
def scheduler():
    schedule.every().day.at("23:11").do(send_all) #Тестил
    while True:
        schedule.run_pending()
        time.sleep(1)

# Запуск
threading.Thread(target=scheduler, daemon=True).start()
print("Бот запущен!")
bot.polling(none_stop=True, interval=0, timeout=3)