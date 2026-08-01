import requests
import time

# ===== НАСТРОЙКИ =====
USER_TOKEN = ""
GUILD_ID = 1234567890
TARGET_USER_ID = 1234567890
CHECK_INTERVAL = 1
# =====================

headers = {
    "Authorization": USER_TOKEN,
    "Content-Type": "application/json"
}

# Выбор режима
print("=" * 50)
print("ВЫБЕРИ РЕЖИМ:")
print("1 - Только микрофон")
print("2 - Только звук (Deafen)")
print("3 - Микрофон + звук")
choice = input("Выбери (1/2/3): ").strip()

if choice == "1":
    MODE = "MIC"
    MODE_NAME = "ТОЛЬКО МИКРОФОН"
    MODE_JSON = {"mute": True}
elif choice == "2":
    MODE = "SOUND"
    MODE_NAME = "ТОЛЬКО ЗВУК"
    MODE_JSON = {"deaf": True}
else:
    MODE = "BOTH"
    MODE_NAME = "МИКРОФОН + ЗВУК"
    MODE_JSON = {"mute": True, "deaf": True}

def get_username(user_id):
    url = f"https://discord.com/api/v9/users/{user_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('username', str(user_id))
    return str(user_id)

print("=" * 60)
print("ТОПОВЫЙ ДИСКОРД БОТ")
print("=" * 60)

# Проверяем токен
check = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
if check.status_code != 200:
    print("Токен не работает!")
    exit()

user_data = check.json()
print(f"Бот запущен от: {user_data['username']}")
print()

# Получаем имя жертвы
victim_name = get_username(TARGET_USER_ID)
print(f"Цель: {victim_name} (ID: {TARGET_USER_ID})")
print(f"Режим: {MODE_NAME}")
print(f"Интервал: {CHECK_INTERVAL} сек")
print()
print("📌 Нажмите Ctrl+C для остановки")
print("-" * 60)

count = 0
success = 0
failed = 0

try:
    while True:
        count += 1
        url = f"https://discord.com/api/v9/guilds/{GUILD_ID}/members/{TARGET_USER_ID}"
        response = requests.patch(url, headers=headers, json=MODE_JSON)
        
        if response.status_code == 204:
            success += 1
            if MODE == "MIC":
                print(f"[{time.strftime('%H:%M:%S')}]  {victim_name} | #{count} | МИКРОФОН ВЫКЛЮЧЕН")
            elif MODE == "SOUND":
                print(f"[{time.strftime('%H:%M:%S')}]  {victim_name} | #{count} | ЗВУК ВЫКЛЮЧЕН")
            else:
                print(f"[{time.strftime('%H:%M:%S')}]  {victim_name} | #{count} | МИКРОФОН + ЗВУК ВЫКЛЮЧЕНЫ")
        elif response.status_code == 403:
            failed += 1
            print(f"[{time.strftime('%H:%M:%S')}]  {victim_name} | #{count} | НЕТ ПРАВ!")
        elif response.status_code == 404:
            failed += 1
            print(f"[{time.strftime('%H:%M:%S')}]  {victim_name} | #{count} | ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН!")
        else:
            failed += 1
            print(f"[{time.strftime('%H:%M:%S')}]  {victim_name} | #{count} | ОШИБКА: {response.status_code}")
    
        time.sleep(CHECK_INTERVAL)
        
except KeyboardInterrupt:
    print("\n" + "=" * 60)
    print(" СТАТИСТИКА:")
    print(f"   Всего попыток: {count}")
    print(f"   Успешно: {success}")
    print(f"   Ошибок: {failed}")
    print("=" * 60)
    print("Остановка бота...")