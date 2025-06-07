from firebase_notify import send_fcm_notification
from gmail_notifier import send_event_email

#最下面有測試範例 就是前端要怎麼送資料進來

# ✅ 通知對照表
NOTIFICATION_CONFIG = {
    "booking_created": {"method": "email"},
    "deal_completed": {"method": "email"},
    "new_rating": {"method": "fcm"},
    "new_food_nearby": {"method": "fcm"},
    "booking_cancelled": {"method": "email"},
    "food_expiring": {"method": "fcm"},
    "pickup_reminder": {"method": "fcm"},
}

# ✅ FCM 樣板（可擴充為多語系）
FCM_TEMPLATES = {
    "new_rating": lambda user, item: ("📮 收到新評價", f"{user} 給了你對「{item}」的評價，來看看吧！"),
    "new_food_nearby": lambda user, item: ("🍱 附近上架新食物", f"你附近剛上架「{item}」，快去預約！"),
    "food_expiring": lambda user, item: ("⌛ 食物即將過期", f"「{item}」即將過期，快來領取吧！"),
    "pickup_reminder": lambda user, item: ("⏰ 領取提醒", f"您預約的「{item}」快到時間了，記得準時！")
}

# ✅ 主函式：根據事件類型自動決定發送方式
def dispatch_notification(event_type, user_name, item_name, email=None, fcm_token=None):
    if event_type not in NOTIFICATION_CONFIG:
        print("❌ 無此通知事件")
        return

    method = NOTIFICATION_CONFIG[event_type]["method"]

    if method == "email":
        if not email:
            print("❌ 缺少 email")
            return
        send_event_email(email, event_type, user_name, item_name)

    elif method == "fcm":
        if not fcm_token:
            print("❌ 缺少 FCM token")
            return
        if event_type not in FCM_TEMPLATES:
            print("❌ 無此 FCM 模板")
            return
        title, body = FCM_TEMPLATES[event_type](user_name, item_name)
        send_fcm_notification(fcm_token, title, body)

    else:
        print("❌ 未知通知方式")

# ✅ 測試範例
# from notify_dispatcher import dispatch_notification

# # 寄 Email 通知：預約已成立
# dispatch_notification(
#     event_type="booking_created",
#     user_name="小美",
#     item_name="三明治便當",
#     email="user@example.com"
# )

# # 發 FCM 推播：附近有新上架食物
# dispatch_notification(
#     event_type="new_food_nearby",
#     user_name="小美",
#     item_name="香蕉蛋糕",
#     fcm_token="e6W_LCbYKvLHLV8XOkVx2i:APA91bG-..."
# )
