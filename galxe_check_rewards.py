import json
import requests

with open("accounts_galxe.json") as f:
    accounts = json.load(f)

print("Galxe Wallet Score Checker (top 20 accounts):\n")

for acc in accounts[:20]:  # Перевіримо перші 20 акаунтів
    wallet = acc["wallet"]
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
        print(f"{wallet} → Galxe Score: {score}")
    except Exception as e:
        print(f"{wallet} → Error: {e}")
