import json
import requests
import random
import time

print("Galxe Smart Wallet Score Checker + Proxy Filter (no Telegram)\n")

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

bad_proxies = set()
used_proxies = set()

def get_working_proxy():
    for _ in range(20):  # до 20 спроб знайти живий проксі
        proxy = random.choice(proxy_lines)
        if proxy in bad_proxies:
            continue
        ip, port, user, pwd = proxy.split(":")
        proxy_dict = {
            "http": f"http://{user}:{pwd}@{ip}:{port}",
            "https": f"http://{user}:{pwd}@{ip}:{port}"
        }
        return proxy, proxy_dict
    return None, None

log_file = open("rewards_log.txt", "w")
dead_log = open("bad_proxies.txt", "w")

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
        proxy_str, proxy_dict = get_working_proxy()
        if not proxy_dict:
            print("[ERROR] Немає робочих проксі")
            break
        try:
            r = requests.post(url, json=payload, proxies=proxy_dict, timeout=15)
            data = r.json()
            score_data = data.get("data", {}).get("identity", {}).get("scores", [])
            score = next((x["score"] for x in score_data if x["platform"] == "GALXE"), "N/A")
            print(f"[OK] {wallet} → Galxe Score: {score}")
            log_file.write(f"{wallet} → Galxe Score: {score}\n")
            used_proxies.add(proxy_str)
            break
        except Exception as e:
            print(f"[RETRY {attempt+1}] {wallet} → {e}")
            bad_proxies.add(proxy_str)
            attempt += 1
            time.sleep(1)

log_file.close()

for proxy in bad_proxies:
    dead_log.write(proxy + "\n")
dead_log.close()
