import json
import requests
import random
import time

BOT_TOKEN = "7679171745:AAG2ElvAtIWTOG7WQuj7jQWTfQBXx0EUwKI"
CHAT_ID = "6821675571"

print("Galxe Smart Wallet Score Checker via Proxy (top 250 accounts):\n")

try:
    with open("accounts_galxe.json") as f:
        accounts = json.load(f)
except Exception as e:
    print(f"[ERROR] Не знайдено accounts_galxe.json: {e}")
    exit()

try:
    with open("proxies.txt") as f:
        proxy_lines = f.read().splitlines()
except Exception as e:
    print(f"[ERROR] Не знайдено proxies.txt: {e}")
    exit()

def get_proxy():
    proxy = random.choice(proxy_lines)
    ip, port, user, pwd = proxy.split(":")
    return {
        "http": f"http://{user}:{pwd}@{ip}:{port}",
        "https": f"http://{user}:{pwd}@{ip}:{port}"
    }

success_log = []
log_file = open("rewards_log.txt", "w")

for acc in accounts:
    wallet = acc.get("wallet", "")
    if not wallet:
        continue

    print(f"[INFO] Перевіряю: {wallet}")
    url = "https://graphigo.prd.galxe.com/query"
    payload = {
        "operationName": "identity",
        "variables": {"id": wallet, "platform": "ETH"},
        "query": "query identity($id: String!, $platform: String!) { identity(platform: $platform, identity: $id) { id address domains scores { score platform } } }"
    }

    attempt = 0
    score = "N/A"
    while attempt < 3:
        try:
            r = requests.post(url, json=payload, proxies=get_proxy(), timeout=15)
            data = r.json()
            score_data = data.get("data", {}).get("identity", {}).get("scores", [])
            score = next((x["score"] for x in score_data if x["platform"] == "GALXE"), "N/A")
            print(f"[OK] {wallet} → Galxe Score: {score}")
            log_file.write(f"{wallet} → Galxe Score: {score}\n")
            if score != "N/A":
                success_log.append(f"{wallet} → Score: {score}")
            break
        except Exception as e:
            print(f"[RETRY {attempt+1}] {wallet} → {e}")
            attempt += 1
            time.sleep(1)

log_file.close()

if success_log:
    message = "Galxe Score Checker (успішно):\n\n" + "\n".join(success_log[:20])
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params={
        "chat_id": CHAT_ID,
        "text": message
    })
else:
    print("[INFO] Немає успішних результатів для надсилання.")
