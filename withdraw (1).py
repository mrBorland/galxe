import json

rate_per_view = 0.01  # $0.01 за перегляд

try:
    with open("youtube_view_log.txt") as f:
        lines = f.readlines()
except:
    lines = []

ok_views = [l for l in lines if "[OK]" in l]
amount = len(ok_views) * rate_per_view

print(f"[INFO] Переглядів: {len(ok_views)}")
print(f"[INFO] Сума до виводу: ${amount:.2f}")

# Тут вставити логіку реального виводу через API/бота
# Наприклад: надсилання на Payeer, USDT, Binance тощо
