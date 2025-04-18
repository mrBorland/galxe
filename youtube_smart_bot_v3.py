import requests
import random
import time
import re
import json

TELEGRAM_TOKEN = "7679171745:AAG2ElvAtIWTOG7WQuj7jQWTfQBXx0EUwKI"
CHAT_ID = "6821675571"

print("YouTube Smart View Bot v3: Аккаунти + Telegram + cookies\n")

SEARCH_KEYWORDS = [
    "airdrop crypto", "earn crypto 2024", "galxe quest", "zealy tutorial", "crypto airdrops"
]

BASE_URL = "https://www.youtube.com/results?search_query={}"

try:
    with open("accounts_youtube.json") as f:
        accounts = json.load(f)
except Exception as e:
    print(f"[ERROR] accounts_youtube.json: {e}")
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

def find_video_links(text):
    return re.findall(r'/watch\?v=[\w-]{11}', text)

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, data=data, timeout=5)
    except:
        pass

log_file = open("youtube_view_log.txt", "a")
success = 0
fail = 0

for i, acc in enumerate(accounts):
    keyword = random.choice(SEARCH_KEYWORDS)
    proxy_dict = get_proxy_dict(acc["proxy"])
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com/",
        "Connection": "keep-alive",
        "Cookie": acc["cookies"]
    }

    print(f"[{i+1}] Аккаунт: {acc['name']} | Пошук: '{keyword}'")
    try:
        search_url = BASE_URL.format(keyword.replace(" ", "+"))
        r = requests.get(search_url, headers=headers, proxies=proxy_dict, timeout=10)
        video_links = find_video_links(r.text)
        if not video_links:
            print("[FAIL] Відео не знайдено")
            fail += 1
            continue

        video_url = "https://www.youtube.com" + random.choice(video_links)
        print(f"[{i+1}] Перегляд {video_url}")

        r = requests.get(video_url, headers=headers, proxies=proxy_dict, timeout=10)
        if r.status_code == 200:
            print(f"[OK] Перегляд зараховано")
            log_file.write(f"[OK] {acc['name']} | {video_url}\n")
            send_telegram(f"[OK] {acc['name']} переглянув: {video_url}")
            success += 1
        else:
            print(f"[FAIL] Статус: {r.status_code}")
            log_file.write(f"[FAIL] {acc['name']} | статус: {r.status_code}\n")
            send_telegram(f"[FAIL] {acc['name']} | статус: {r.status_code}")
            fail += 1
    except Exception as e:
        print(f"[ERROR] {e}")
        log_file.write(f"[ERROR] {acc['name']} | {e}\n")
        send_telegram(f"[ERROR] {acc['name']} | {e}")
        fail += 1
    time.sleep(1)

log_file.close()
print(f"\nГотово. Переглядів: {success}, Помилок: {fail}. Лог: youtube_view_log.txt")
