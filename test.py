import requests
import json

TOKEN = "8288669449:AAGGeY4yI8SnRCkOmWOlFQ-Yq43n8x-uPWg"

with open('groups.json') as f:
    groups = json.load(f)

messages = {
    "1ip6": " Сообщение для группы 1ip6!",
    "1vr1": " Сообщение для группы 1vr1!"
}

for group_name, user_ids in groups.items():
    print(f"\nГруппа {group_name}:")
    
    for user_id in user_ids:
        try:
            resp = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={"chat_id": user_id, "text": messages[group_name], "parse_mode": "HTML"}
            )
            print(f"  ID {user_id}: {'true' if resp.status_code == 200 else 'false'}")
        except:
            print(f"  ID {user_id}:  Error")