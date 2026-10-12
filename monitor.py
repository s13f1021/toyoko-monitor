import os
import requests
from playwright.sync_api import sync_playwright


DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

HOTEL_URL = "https://www.toyoko-inn.com/search/detail/00281/"

CHECKIN = "2026-11-28"
CHECKOUT = "2026-11-29"


def send_discord(message):

    payload = {
        "content": message
    }

    requests.post(
        DISCORD_WEBHOOK_URL,
        json=payload,
        timeout=10
    )


def check_room():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            HOTEL_URL,
            wait_until="networkidle",
            timeout=60000
        )

        # ここで
        # チェックイン
        # チェックアウト
        # 大人2名
        # ツイン
        # を指定する

        # 現在の東横INN予約画面に合わせて
        # セレクターを設定する

        browser.close()

        return False


if __name__ == "__main__":

    available = check_room()

    if available:

        send_discord(
            "🚨 東横INN空室発見！\n\n"
            "🏨 東横INN新宿御苑前駅3番出口\n"
            "📅 2026/11/28 → 11/29\n"
            "👥 大人2名\n"
            "🛏️ ツイン\n\n"
            "今すぐ予約を確認してください！"
        )

    else:

        print("空室なし")
