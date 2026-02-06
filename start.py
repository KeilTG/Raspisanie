import requests
import json
import time

TOKEN = "8288669449:AAGGeY4yI8SnRCkOmWOlFQ-Yq43n8x-uPWg"
JSON_FILE = "users.json"
last_id = 0
sent_users = set() 

while True:
    r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={"offset": last_id + 1}).json()
    
    if r["ok"] and r["result"]:
        for upd in r["result"]:
            if "message" in upd:
                txt = upd["message"].get("text", "")
                uid = upd["message"]["from"]["id"]
                
                if txt.lower() == "/start" and uid not in sent_users:
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                 json={"chat_id": uid, "text": "Напишите свою группу! \nПример: 1ip6 , 1vr1 , 1rki2 ."})
                    sent_users.add(uid) 
                
                last_id = upd["update_id"]
    
    time.sleep(1)