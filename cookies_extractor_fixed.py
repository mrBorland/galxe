import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

def get_driver(proxy):
    options = uc.ChromeOptions()
    if proxy:
        options.add_argument(f'--proxy-server=http://{proxy}')
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return uc.Chrome(options=options)

def login_and_get_cookies(email, password, proxy):
    try:
        driver = get_driver(proxy)
        driver.get("https://accounts.google.com/ServiceLogin")

        time.sleep(3)
        driver.find_element(By.ID, "identifierId").send_keys(email)
        driver.find_element(By.ID, "identifierNext").click()
        time.sleep(3)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.ID, "passwordNext").click()
        time.sleep(5)

        cookies = driver.get_cookies()
        cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        driver.quit()
        return cookie_string
    except Exception as e:
        print(f"[ERROR] {email} — {e}")
        try: driver.quit()
        except: pass
        return None

with open("accounts_raw.txt") as f:
    accounts = [line.strip().split(":") for line in f if ":" in line]

with open("proxies.txt") as f:
    proxies = [line.strip() for line in f if line.strip()]

cookies_list = []
accounts_output = []

for i, (email, password) in enumerate(accounts):
    proxy = proxies[i % len(proxies)]
    print(f"[{i+1}] Авторизація через проксі {proxy}")
    cookie = login_and_get_cookies(email, password, proxy)
    if cookie:
        cookies_list.append(cookie)
        accounts_output.append({
            "name": f"user{i+1}",
            "cookies": cookie,
            "proxy": proxy
        })

with open("cookies_list.txt", "w") as f:
    f.write("\n".join(cookies_list))

with open("accounts_youtube.json", "w") as f:
    json.dump(accounts_output, f, indent=2)

print(f"[DONE] Успішно додано {len(cookies_list)} акаунтів з cookies")
