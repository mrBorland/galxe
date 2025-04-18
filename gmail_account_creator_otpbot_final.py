import time
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import telebot

BOT_TOKEN = "7739907978:AAEfzWxMHySj-YtwJMx2V4hIloW4zAzAYcE"
CHAT_ID = "6821675571"

bot = telebot.TeleBot(BOT_TOKEN)

def get_number_from_otpbot():
    bot.send_message(CHAT_ID, "/getnumber")
    print("[OTPBot] Очікування номера...")
    for _ in range(60):
        updates = bot.get_updates()
        for u in updates[::-1]:
            if u.message and u.message.text.startswith("+"):
                return u.message.text
        time.sleep(3)
    return None

def get_sms_code_from_otpbot():
    print("[OTPBot] Очікування SMS-коду...")
    for _ in range(60):
        updates = bot.get_updates()
        for u in updates[::-1]:
            if u.message and any(char.isdigit() for char in u.message.text) and len(u.message.text.strip()) <= 8:
                return u.message.text.strip()
        time.sleep(3)
    return None

def create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return uc.Chrome(options=options)

def register_account(email_prefix):
    phone = get_number_from_otpbot()
    if not phone:
        print("[ERROR] Номер не отримано")
        return None

    driver = create_driver()
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

        driver.find_element(By.ID, "phoneNumberId").send_keys(phone)
        driver.find_element(By.XPATH, "//span[text()='Next']").click()
        time.sleep(5)

        code = get_sms_code_from_otpbot()
        if not code:
            print("[ERROR] SMS-код не надійшов")
            return None

        driver.find_element(By.NAME, "code").send_keys(code)
        driver.find_element(By.XPATH, "//span[text()='Verify']").click()
        time.sleep(5)

        email = f"{email_prefix}@gmail.com"
        return email, password
    except Exception as e:
        print(f"[FAIL] {e}")
        return None
    finally:
        driver.quit()

def main():
    results = []
    for i in range(5):  # можна змінити на 100 після тесту
        prefix = f"otpuser{i+1}{random.randint(100,999)}"
        acc = register_account(prefix)
        if acc:
            results.append(f"{acc[0]}:{acc[1]}")
            with open("accounts_raw.txt", "a") as f:
                f.write(f"{acc[0]}:{acc[1]}\n")
        else:
            print("[!] Пропущено через помилку")

    print(f"[DONE] Створено {len(results)} акаунтів")

if __name__ == "__main__":
    main()
