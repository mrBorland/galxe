import json
import requests

# ========== Налаштування ==========
rate_per_view = 0.01  # $0.01 за перегляд
TELEGRAM_TOKEN = "7679171745:AAG2ElvAtIWTOG7WQuj7jQWTfQBXx0EUwKI"
CHAT_ID = "6821675571"
MONO_CARD = "4441111073415832"
# ===================================

try:
    with open("youtube_view_log.txt") as f:
        lines = f.readlines()
except FileNotFoundError:
    print("[ERROR] Файл youtube_view_log.txt не знайдено.")
    lines = []

ok_views = [l for l in lines if "[OK]" in l]
amount = len(ok_views) * rate_per_view

message = "[YouTube Bot]\n"
message += f"Переглядів: {len(ok_views)}\n"
message += f"Сума до виводу: ${amount:.2f}\n"
message += f"Вивести на Monobank: {MONO_CARD}"

print(message)

# Надсилання в Telegram
try:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data, timeout=5)
except:
    print("[WARN] Не вдалося надіслати в Telegram")
