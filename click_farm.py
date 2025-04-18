import requests
import random
import time

print("Click Farm Bot: Використання старих проксі для емуляції переглядів/кліків\n")

try:
    with open("proxies.txt") as f:
        proxies = f.read().splitlines()
except Exception as e:
    print(f"[ERROR] Не знайдено proxies.txt: {e}")
    exit()

TARGET_URL = "https://sproutgigs.com/"  # Можна змінити на будь-яку ціль

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_proxy_dict(proxy_str):
    ip, port, user, pwd = proxy_str.split(":")
    return {
        "http": f"http://{user}:{pwd}@{ip}:{port}",
        "https": f"http://{user}:{pwd}@{ip}:{port}"
    }

success = 0
fail = 0

for i in range(len(proxies)):
    proxy = random.choice(proxies)
    proxy_dict = get_proxy_dict(proxy)
    print(f"[{i+1}] Відправляю запит через {proxy}")
    try:
        r = requests.get(TARGET_URL, headers=headers, proxies=proxy_dict, timeout=10)
        if r.status_code == 200:
            print(f"[OK] Успішний запит")
            success += 1
        else:
            print(f"[FAIL] Статус: {r.status_code}")
            fail += 1
    except Exception as e:
        print(f"[ERROR] {e}")
        fail += 1
    time.sleep(1)

print(f"\nГотово. Успішно: {success}, Помилки: {fail}")
