import requests
import time

# ====== CẤU HÌNH ======
API_KEY = "AIzaSyCgxiSwlcUUbtc6bUpZgsXi-Sisstp3Pqg"  # ← YouTube API key của bạn
BOT_TOKEN = "8594443115:AAHCVjy688Gikjvi0sE0h90z3wvCGlsQVFI"  # ← Token bot Telegram
CHAT_ID = "-5044752729"  # ← ID Telegram của bạn

# Danh sách kênh cần theo dõi
CHANNELS = {
    "Pencilmation": "UCUAL--p3qAa27luR0IYbjZA",
    "itsAlexClark": "UCsDmESjqNPukDmVnuneLrqw",
    "TroomTroom": "UCWwqHwqLSrdWMgp5DZG5Dzg",
    "AnnoyingOrange": "UCi-5OZ2tYuwMLIcEyOsbdRA",
    "ExplosmEntertainment": "UCWXCrItCF6ZzXrdozUS-Idw",
    "Domics": "UCn1XB-jvmd9fXMzhiA6IR0w",
    "DaFuqBoom": "UCsSsgPaZ2GSmO6il8Cb5iGA",
    "WiseFoxRobin": "UC-Pd_3rejYcns7Av_jkbqnA",
    "todoko": "uc-xlyxebvbdlo8wx3lnegfq",  # ← kênh của bạn
}

CHECK_INTERVAL = 60  # kiểm tra mỗi 60 giây

# ====== CODE CHÍNH ======
latest_videos = {}

def get_latest_video(channel_id):
    """Lấy video mới nhất bằng YouTube Data API"""
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}&channelId={channel_id}&part=snippet,id"
        f"&order=date&maxResults=1"
    )
    resp = requests.get(url)
    data = resp.json()

    items = data.get("items", [])
    if not items:
        return None, None

    video_id = items[0]["id"].get("videoId")
    title = items[0]["snippet"]["title"]
    return video_id, title


def send_telegram_message(text):
    """Gửi tin nhắn Telegram"""
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(telegram_url, data={"chat_id": CHAT_ID, "text": text})


print("🚀 Bot YouTube Notifier đang chạy...\n")

while True:
    for name, channel_id in CHANNELS.items():
        try:
            video_id, title = get_latest_video(channel_id)
            if not video_id:
                continue

            video_url = f"https://www.youtube.com/watch?v={video_id}"

            if channel_id not in latest_videos:
                latest_videos[channel_id] = video_id
                send_telegram_message(f"📢 {name} - video mới nhất:\n{title}\n{video_url}")

            elif latest_videos[channel_id] != video_id:
                latest_videos[channel_id] = video_id
                send_telegram_message(f"🆕 {name} vừa đăng video mới!\n{title}\n{video_url}")

        except Exception as e:
            print(f"Lỗi khi quét {name}: {e}")
    # Giữ cho Render không "ngủ"
    try:
        requests.get("https://youtube-tele-bot.onrender.com")
    except:
        pass


    time.sleep(CHECK_INTERVAL)
