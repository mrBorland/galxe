import requests
import random
import time

print("YouTube View Bot: Фарм переглядів на вказане відео через проксі\n")

VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # <- сюди вставляється твоє відео

try:
    with open("proxies.txt") as f:
        proxies = f.read().splitlines()
except Exception as e:
    print(f"[ERROR] Не знайдено proxies.txt: {e}")
    exit()

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
]

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
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com/",
        "Connection": "keep-alive"
    }
    print(f"[{i+1}] Перегляд {VIDEO_URL} через {proxy}")
    try:
        r = requests.get(VIDEO_URL, headers=headers, proxies=proxy_dict, timeout=10)
        if r.status_code == 200:
            print(f"[OK] Перегляд зараховано")
            success += 1
        else:
            print(f"[FAIL] Статус: {r.status_code}")
            fail += 1
    except Exception as e:
        print(f"[ERROR] {e}")
        fail += 1
    time.sleep(1)

print(f"\nГотово. Переглядів: {success}, Помилок: {fail}")
