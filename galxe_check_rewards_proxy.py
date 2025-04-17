import json
import requests
import random

print("Galxe Wallet Score Checker via Proxy (top 20 accounts):\n")

# Завантаження акаунтів
try:
    with open("accounts_galxe.json") as f:
        accounts = json.load(f)
except Exception as e:
    print(f"[ERROR] Не знайдено accounts_galxe.json: {e}")
    exit()

# Завантаження проксі
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

for acc in accounts[:20]:
    wallet = acc.get("wallet", "")
    if not wallet:
        print("[SKIP] Порожній гаманець")
        continue

    print(f"[INFO] Перевіряю: {wallet}")
    url = "https://graphigo.prd.galxe.com/query"
    payload = {
        "operationName": "identity",
        "variables": {"id": wallet, "platform": "ETH"},
        "query": "query identity($id: String!, $platform: String!) { identity(platform: $platform, identity: $id) { id address domains scores { score platform } } }"
    }
    try:
        r = requests.post(url, json=payload, proxies=get_proxy(), timeout=15)
        data = r.json()
        score_data = data.get("data", {}).get("identity", {}).get("scores", [])
        score = next((x["score"] for x in score_data if x["platform"] == "GALXE"), "N/A")
        print(f"[OK] {wallet} → Galxe Score: {score}")
    except Exception as e:
        print(f"[ERROR] {wallet} → {e}")
