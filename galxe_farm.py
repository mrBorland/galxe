import json
import time
import random
import requests

from fake_useragent import UserAgent

ACCOUNTS_FILE = 'accounts.json'
PROXIES_FILE = 'proxies_galxe.txt'
TELEGRAM_TOKEN = '7679171745:AAG2ElvAtIWTOG7jQWTfQBXx0EUwKI'
TELEGRAM_CHAT_ID = '6821675571'
LOG_FILE = 'farm_log.txt'

def load_accounts():
    with open(ACCOUNTS_FILE, 'r') as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def load_proxies():
    with open(PROXIES_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def send_telegram(message):
    try:
        url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
        requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message})
    except:
        pass

def log(text):
    with open(LOG_FILE, 'a') as f:
        f.write(text + '\n')
    print(text)
    send_telegram(text)

def perform_galxe_tasks(account, proxy=None):
    headers = {
        "User-Agent": UserAgent().random,
        "Content-Type": "application/json"
    }

    time.sleep(random.randint(2, 5))
    log(f"[+] {account['email']} виконав завдання на Galxe (імітація)")
    return True

def main():
    accounts = load_accounts()
    proxies = load_proxies()

    log(f"=== Старт фарму Galxe для {len(accounts)} акаунтів ===")

    for i, account in enumerate(accounts):
        proxy = proxies[i % len(proxies)]

        try:
            success = perform_galxe_tasks(account, proxy)
            if not success:
                log(f"[-] {account['email']} — завдання не виконані")
        except Exception as e:
            log(f"[X] {account['email']} — помилка: {str(e)}")

        time.sleep(random.randint(2, 4))

    log("=== Фарм Galxe завершено ===")

if __name__ == "__main__":
    main()
