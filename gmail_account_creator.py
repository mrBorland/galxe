import requests
import random
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

SMS_API_KEY = "48d90e3f324082751B9422c54B59e99d"

def get_proxy_list():
    with open("proxies.txt") as f:
        return [line.strip() for line in f if line.strip()]

def get_sms_number():
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_API_KEY}&action=getNumber&service=go&country=0"
    resp = requests.get(url).text
    if "ACCESS_NUMBER" in resp:
        parts = resp.split(":")
        return parts[1], parts[2]  # id, number
    return None, None

def get_sms_code(id):
    for _ in range(60):
        time.sleep(5)
        resp = requests.get(f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_API_KEY}&action=getStatus&id={id}").text
        if "STATUS_OK" in resp:
            return resp.split(":")[1]
    return None

def complete_sms(id):
    requests.get(f"https://api.sms-activate.org/stubs/handler_api.php?api_key={SMS_API_KEY}&action=setStatus&status=6&id={id}")

def create_driver(proxy):
    options = uc.ChromeOptions()
    if proxy:
        options.add_argument(f'--proxy-server=http://{proxy}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless=new")
    return uc.Chrome(options=options)

def register_gmail(email_prefix, proxy):
    id, number = get_sms_number()
    if not number:
        print("[ERROR] Не вдалося отримати номер")
        return None

    driver = create_driver(proxy)
    try:
        driver.get("https://accounts.google.com/signup")
        time.sleep(3)

        driver.find_element(By.ID, "firstName").send_keys("Taras")
        driver.find_element(By.ID, "lastName").send_keys("Bot")
        driver.find_element(By.ID, "username").send_keys(email_prefix)
        password = f"Pass{random.randint(1000,9999)}!"
        driver.find_element(By.NAME, "Passwd").send_keys(password)
        driver.find_element(By.NAME, "ConfirmPasswd").send_keys(password)
        driver.find_element(By.XPATH, "//span[text()='Next']").click()
        time.sleep(5)

        driver.find_element(By.ID, "phoneNumberId").send_keys("+" + number)
        driver.find_element(By.XPATH, "//span[text()='Next']").click()
        time.sleep(5)

        code = get_sms_code(id)
        if not code:
            print("[ERROR] Код не отримано")
            return None

        driver.find_element(By.NAME, "code").send_keys(code)
        driver.find_element(By.XPATH, "//span[text()='Verify']").click()
        time.sleep(5)
        complete_sms(id)

        email = f"{email_prefix}@gmail.com"
        return email, password
    except Exception as e:
        print(f"[FAIL] {e}")
        return None
    finally:
        driver.quit()

def main():
    proxies = get_proxy_list()
    results = []
    for i in range(100):
        prefix = f"userbot{i+1}{random.randint(100,999)}"
        proxy = proxies[i % len(proxies)]
        print(f"[{i+1}] Реєстрація з проксі: {proxy}")
        acc = register_gmail(prefix, proxy)
        if acc:
            results.append(f"{acc[0]}:{acc[1]}")
            with open("accounts_raw.txt", "a") as f:
                f.write(f"{acc[0]}:{acc[1]}\n")
        else:
            print("[!] Пропущено через помилку")

    print(f"[DONE] Створено {len(results)} акаунтів")

if __name__ == "__main__":
    main()
