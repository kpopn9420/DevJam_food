# firebase_messaging.py
import firebase_admin
from firebase_admin import credentials, messaging
import os

# ✅ 只初始化一次
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")  # 你的 JSON 金鑰檔
    firebase_admin.initialize_app(cred)

# ✅ 發送通知主函式
def send_fcm_notification(token, title, body, data=None):
    """
    發送推播通知給指定 token
    :param token: 裝置 token
    :param title: 通知標題
    :param body: 通知內文
    :param data: 自訂 data payload（選填）
    """
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
            data=data or {}
        )
        response = messaging.send(message)
        print("✅ Notification sent:", response)
        return True
    except Exception as e:
        print("❌ Failed to send notification:", e)
        return False
