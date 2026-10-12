import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://www.toyoko-inn.com/search/result/?area=5287&people=2&room=1&smoking=all&start=2026-11-28&end=2026-11-29&r_avail_only=true"

NO_RESULT_TEXT = "一致する検索結果はありません"

DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]


def send_discord(message):
    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json={"content": message},
        timeout=20
    )
    response.raise_for_status()


def check_page():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            locale="ja-JP"
        )

        try:
            page.goto(
                URL,
                wait_until="networkidle",
                timeout=60000
            )

            page.wait_for_timeout(3000)

            text = page.locator("body").inner_text()

            print("ページ取得完了")
            print(f"ページ文字数: {len(text)}")

            if NO_RESULT_TEXT in text:
                print("空室なし")
                return False

            print("検索結果あり → Discord通知")
            return True

        finally:
            browser.close()


if __name__ == "__main__":

    try:
        available = check_page()

        if available:
            send_discord(
                "🚨 東横INNに空室が出ました！\n\n"
                "🏨 東横INN 新宿御苑前駅3番出口\n"
                "📅 2026/11/28 → 11/29\n"
                "👥 2名\n"
                "🛏️ ツイン検索\n\n"
                "今すぐ確認してください！\n"
                f"{URL}"
            )

    except Exception as e:

        print(f"エラー: {e}")
        raise
