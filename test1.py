# 先導入後面會用到的套件
import requests
from bs4 import BeautifulSoup
import time


# ==== 設定區 ====
TOKEN = "8468047449:AAHp6Hx8pBKOB7hGiKYp3CkYzQP7zmniZbg"
CHAT_ID = "7139263879"

# 要爬的股票
stock_list = ["1101", "2330", "1102"]

# HTTP 請求標頭
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


# ==== Telegram 發送函式 ====
def send_telegram_message(token, chat_id, message):
    """使用 Telegram Bot 發送訊息"""
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        response = requests.get(
            url,
            params={
                "chat_id": chat_id,
                "text": message
            },
            timeout=10
        )

        response.raise_for_status()

        print("Telegram 訊息發送成功")

    except requests.exceptions.RequestException as e:
        print(f"Telegram 發送失敗：{e}")


# ==== 爬取股票 ====
for stock_id in stock_list:

    try:
        # Yahoo 股市網址
        url = f"https://tw.stock.yahoo.com/quote/{stock_id}.TW"

        # 發送請求
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        # 解析 HTML
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # 找出股價
        price_tag = soup.find(
            "span",
            class_=lambda x: x and "Fz(32px)" in x
        )

        # 如果找不到
        if price_tag is None:
            print(
                f"股票 {stock_id} 抓不到股價，"
                "可能是 Yahoo 網頁結構已改變"
            )
            continue

        # 取得股價文字
        price = price_tag.get_text(strip=True)

        # 建立訊息
        message = f"股票 {stock_id} 即時股價為 {price}"

        # 顯示在 Python
        print(message)

        # 傳送 Telegram
        send_telegram_message(
            TOKEN,
            CHAT_ID,
            message
        )

    except requests.exceptions.RequestException as e:

        print(
            f"抓取股票 {stock_id} 時發生錯誤：{e}"
        )

    # 每支股票間隔 3 秒
    time.sleep(3)
