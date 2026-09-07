# 先導入後面會用到的套件
import requests  # 請求工具
from bs4 import BeautifulSoup  # 解析工具
import time  # 用來暫停程式

# ==== 設定區（建議放在迴圈外，只設定一次）====
TOKEN = "輸入你的 bot token"
CHAT_ID = "輸入你的 telegram id"

# 要爬的股票
stock_list = ["1101", "2330", "1102"]

# 可能的股價 class（漲/跌/平盤）
price_classes = [
    "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)",
    "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)",
    "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)",
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def send_telegram_message(token, chat_id, message):
    """用 telegram bot 送訊息，並做基本錯誤處理"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.get(url, params={"chat_id": chat_id, "text": message}, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Telegram 發送失敗: {e}")

for stockid in stock_list:  # 迴圈依序爬股價
    try:
        # 網址塞入股票編號
        url = f"https://tw.stock.yahoo.com/quote/{stockid}.TW"
        # 發送請求
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        # 解析回應的 HTML
        soup = BeautifulSoup(r.text, "html.parser")
        # 定位股價
        price_tag = soup.find("span", class_=price_classes)

        if price_tag is None:
            print(f"股票 {stockid} 抓不到股價，可能是網頁結構已改變")
            continue

        price = price_tag.get_text()
        # 回報的訊息（可自訂）
        message = f"股票 {stockid} 即時股價為 {price}"
        print(message)

        # 用 telegram bot 回報股價
        send_telegram_message(TOKEN, CHAT_ID, message)

    except requests.exceptions.RequestException as e:
        print(f"抓取股票 {stockid} 時發生錯誤: {e}")

    # 每次都停 3 秒
    time.sleep(3)
