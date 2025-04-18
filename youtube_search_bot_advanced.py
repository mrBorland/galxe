import requests
import random
import time
from bs4 import BeautifulSoup

print("YouTube Smart View Bot: Пошук відео за ключем + ротація + логування\n")

SEARCH_KEYWORDS = [
    "airdrop crypto",
    "earn crypto 2024",
    "galxe quest",
    "zealy tutorial",
    "crypto airdrops"
]

BASE_URL = "https://www.youtube.com/results?search_query={}"

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

def get_random_video_url(proxy_dict, headers, keyword):
    try:
        search_url = BASE_URL.format(keyword.replace(" ", "+"))
        r = requests.get(search_url, headers=headers, proxies=proxy_dict, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        video_links = [
            "https://www.youtube.com" + link.get("href")
            for link in soup.find_all("a")
            if link.get("href") and "/watch?v=" in link.get("href")
        ]
        if video_links:
            return random.choice(video_links)
    except Exception as e:
        print(f"[SEARCH ERROR] {e}")
    return None

success = 0
fail = 0

log_file = open("youtube_view_log.txt", "a")

for i in range(len(proxies)):
    keyword = random.choice(SEARCH_KEYWORDS)
    proxy = random.choice(proxies)
    proxy_dict = get_proxy_dict(proxy)
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com/",
        "Connection": "keep-alive"
    }

    print(f"[{i+1}] Пошук відео за ключем: '{keyword}' через {proxy}")
    video_url = get_random_video_url(proxy_dict, headers, keyword)
    if not video_url:
        print("[FAIL] Відео не знайдено")
        fail += 1
        continue

    print(f"[{i+1}] Перегляд {video_url}")
    try:
        r = requests.get(video_url, headers=headers, proxies=proxy_dict, timeout=10)
        if r.status_code == 200:
            print(f"[OK] Перегляд зараховано")
            log_file.write(f"[OK] {video_url} | проксі: {proxy}\n")
            success += 1
        else:
            print(f"[FAIL] Статус: {r.status_code}")
            log_file.write(f"[FAIL] {video_url} | статус: {r.status_code} | проксі: {proxy}\n")
            fail += 1
    except Exception as e:
        print(f"[ERROR] {e}")
        log_file.write(f"[ERROR] {video_url} | {e} | проксі: {proxy}\n")
        fail += 1
    time.sleep(1)

log_file.close()
print(f"\nГотово. Переглядів: {success}, Помилок: {fail}. Лог: youtube_view_log.txt")
