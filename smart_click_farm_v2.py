import requests
import random
import time

print("Smart Click Farm v2: YouTube, Microworkers, SproutGigs — без проблемних цілей\n")

try:
    with open("proxies.txt") as f:
        proxies = f.read().splitlines()
except Exception as e:
    print(f"[ERROR] Не знайдено proxies.txt: {e}")
    exit()

TARGET_URLS = [
    "https://www.youtube.com/",
    "https://sproutgigs.com/",
    "https://microworkers.com/"
]

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
    target = random.choice(TARGET_URLS)
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://google.com/"
    }
    print(f"[{i+1}] Клік по {target} через {proxy}")
    try:
        r = requests.get(target, headers=headers, proxies=proxy_dict, timeout=10)
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
