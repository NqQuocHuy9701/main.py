from telethon import TelegramClient, events
from datetime import datetime
import json
import os

# ---- THÔNG SỐ BOT ----
api_id = 1234567          # API ID của bạn
api_hash = "your_api_hash"
bot_token = "your_bot_token"

# ---- TÊN FILE LƯU LOG ----
TEXT_LOG = "log.txt"
JSON_LOG = "log.json"

# ---- KHỞI TẠO FILE LOG ----
if not os.path.exists(JSON_LOG):
    with open(JSON_LOG, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)


client = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)


# ---- HÀM GHI LOG ----
def save_log(username, action, time_raw):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ghi text
    with open(TEXT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{now} | {username} | {action} | {time_raw}\n")

    # Ghi json
    with open(JSON_LOG, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.append({
        "timestamp": now,
        "username": username,
        "action": action,
        "time": time_raw
    })

    with open(JSON_LOG, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---- LẮNG NGHE TIN NHẮN ----
@client.on(events.NewMessage(pattern=r"#checkin|#checkout|#checkin|#check_out"))
async def handler(event):
    text = event.raw_text.lower()

    username = event.sender.username or event.sender.first_name
    time_raw = text.replace("#checkin", "").replace("#checkout", "").strip()

    if "#checkin" in text:
        action = "checkin"
    elif "#checkout" in text:
        action = "checkout"
    else:
        return  # không phải cú pháp → bỏ qua

    save_log(username, action, time_raw)

    # Phản hồi gọn
    await event.reply(f"Đã ghi log cho **{username}**: {action.upper()} lúc {time_raw}")


print("Bot đang chạy...")
client.run_until_disconnected()
