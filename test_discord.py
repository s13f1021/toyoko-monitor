import os
import requests

url = os.environ["DISCORD_WEBHOOK_URL"]

response = requests.post(
    url,
    json={
        "content": (
            "🧪 東横INN空室監視テスト\n"
            "Discord通知は正常に動作しています！\n"
            "対象日：2026/11/28〜11/29"
        )
    },
    timeout=20
)

response.raise_for_status()
print("Discord通知成功")
