import requests
import json
import time

TOKEN = "8288669449:AAGGeY4yI8SnRCkOmWOlFQ-Yq43n8x-uPWg"
JSON_FILE = "users.json"
last_id = 0

try:
    with open('groups.json', 'r') as f:
        groups = json.load(f)
except:
    groups = {"1ip6": [], "1vr1": []}

while True:
    r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={"offset": last_id + 1}).json()
    
    if r["ok"] and r["result"]:
        for upd in r["result"]:
            if "message" in upd:
                txt = upd["message"].get("text", "").lower()
                uid = upd["message"]["from"]["id"]
                
                if txt == "1ip6":
                    groups["1ip6"].append(uid) if uid not in groups["1ip6"] else None
                elif txt == "1vr1":
                    groups["1vr1"].append(uid) if uid not in groups["1vr1"] else None
                
                if txt in ["1ip6", "1vr1"]:
                    with open('groups.json', 'w') as f:
                        json.dump(groups, f)
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": uid, "text": f"Добавлен в {txt[0::]}"})
                
                last_id = upd["update_id"]
    
    time.sleep(1)