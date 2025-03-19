import asyncio
import json
import os
import sqlite3
from telethon import TelegramClient, errors


async def check_sessions():
    session_files = [f for f in os.listdir() if f.endswith(".session")]

    for session_file in session_files:
        session_name = os.path.splitext(session_file)[0]
        json_file = f"{session_name}.json"

        if not os.path.exists(json_file):
            print(f"❌ JSON для {session_name} не найден, пропускаем")
            continue

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            api_id = 21952430
            api_hash = "5e1498b87cff685f05659a6a4fe34f30"
        except (json.JSONDecodeError, KeyError) as e:
            print(f"❌ Ошибка в JSON {json_file}: {e}")
            continue

        try:
            conn = sqlite3.connect(session_file)
            conn.execute("PRAGMA integrity_check")
            conn.close()
        except sqlite3.DatabaseError:
            print(f"❌ Повреждённая сессия: {session_name}, пропускаем")
            continue

        try:
            client = TelegramClient(session_name, api_id, api_hash)
            await client.connect()

            if await client.is_user_authorized():
                print(f"✅ Сессия {session_name} работает")
            else:
                print(f"❌ Сессия {session_name} не авторизована, пропускаем")

            await client.disconnect()
        except errors.SessionPasswordNeededError:
            print(f"❌ Сессия {session_name} требует пароль, пропускаем")
        except Exception as e:
            print(f"❌ Ошибка сессии {session_name}: {e}")


if __name__ == "__main__":
    asyncio.run(check_sessions())
