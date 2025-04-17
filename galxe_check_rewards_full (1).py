import json
import requests

print("Galxe Wallet Score Checker (всі 250 акаунтів):\n")

try:
    with open("accounts_galxe.json") as f:
        accounts = json.load(f)
except Exception as e:
    print(f"[ERROR] Не знайдено файл accounts_galxe.json: {e}")
    exit()

with open("reward_log.txt", "w") as log:
    for acc in accounts:
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
            r = requests.post(url, json=payload, timeout=10)
            data = r.json()
            score_data = data.get("data", {}).get("identity", {}).get("scores", [])
            score = next((x["score"] for x in score_data if x["platform"] == "GALXE"), "N/A")
            result = f"[OK] {wallet} → Galxe Score: {score}"
            print(result)
            log.write(result + "\n")
        except Exception as e:
            error = f"[ERROR] {wallet} → {e}"
            print(error)
            log.write(error + "\n")
