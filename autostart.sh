#!/data/data/com.termux/files/usr/bin/bash

cd ~/fixbot/galxe

while true
do
    echo "[START] $(date)"
    python youtube_smart_bot_v3.py
    python withdraw.py
    echo "[WAIT] Очікування 6 годин..."
    sleep 21600  # 6 годин = 21600 секунд
done
