import requests
import random

print("Proxy Tester: перевірка всіх проксі (HTTPS support for Galxe API)\n")

try:
    with open("proxies.txt") as f:
        proxies = f.read().splitlines()
except Exception as e:
    print(f"[ERROR] Не знайдено proxies.txt: {e}")
    exit()

alive = []
bad = []

for proxy in proxies:
    try:
        ip, port, user, pwd = proxy.strip().split(":")
        proxy_dict = {
            "http": f"http://{user}:{pwd}@{ip}:{port}",
            "https": f"http://{user}:{pwd}@{ip}:{port}"
        }
        r = requests.post("https://graphigo.prd.galxe.com/query", timeout=10, proxies=proxy_dict)
        if r.status_code in [200, 400]:  # 400 - нормальний response Galxe без payload
            print(f"[LIVE] {proxy}")
            alive.append(proxy)
        else:
            print(f"[BAD] {proxy} → Status: {r.status_code}")
            bad.append(proxy)
    except Exception as e:
        print(f"[BAD] {proxy} → {e}")
        bad.append(proxy)

# Зберегти тільки робочі проксі
with open("proxies_alive.txt", "w") as f:
    for proxy in alive:
        f.write(proxy + "\n")

print(f"\nГотово. Робочих проксі: {len(alive)}, Мертвих: {len(bad)}")
