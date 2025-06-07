from firebase_admin import credentials, initialize_app, messaging
import firebase_admin
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# ✅ 初始化 Firebase 一次
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    initialize_app(cred)

# ✅ Gmail 設定
GMAIL_USER = 'be.happy.forever717@gmail.com'
GMAIL_PASS = 'paoajteekhhnvxxj'

# ✅ 支援的通知事件及模板
NOTIFICATION_TEMPLATES = {
    "booking_created": {
        "subject": "預約已成立！",
        "message": lambda user, item: f"您好 {user}，您已成功預約「{item}」，請準時領取。",
        "title": "✅ 預約成立",
        "body": lambda user, item: f"您已成功預約「{item}」，請記得領取喔！"
    },
    "deal_completed": {
        "subject": "交易完成通知",
        "message": lambda user, item: f"您好 {user}，您與對方的「{item}」交易已完成，歡迎留下評價！",
        "title": "✅ 交易完成",
        "body": lambda user, item: f"您已完成「{item}」交易，記得評價唷！"
    },
    "new_rating": {
        "subject": "您收到一筆新評價",
        "message": lambda user, item: f"您好 {user}，您剛剛收到關於「{item}」的評價，快來看看！",
        "title": "📮 收到新評價",
        "body": lambda user, item: f"{user} 對「{item}」發表了一則新評價"
    },
    "new_food_nearby": {
        "subject": "附近有新上架的食物",
        "message": lambda user, item: f"嘿 {user}，您附近剛上架「{item}」，有興趣看看嗎？",
        "title": "🍱 附近上架新食物",
        "body": lambda user, item: f"附近出現「{item}」！點擊查看詳情"
    },
    "booking_cancelled": {
        "subject": "預約已取消",
        "message": lambda user, item: f"您好 {user}，您預約的「{item}」已被取消，請重新安排。",
        "title": "❌ 預約取消",
        "body": lambda user, item: f"「{item}」預約被取消，點我查看原因"
    },
    "food_expiring": {
        "subject": "食物即將過期提醒",
        "message": lambda user, item: f"提醒您，食物「{item}」即將過期，若有需要請盡快領取。",
        "title": "⌛ 食物快過期",
        "body": lambda user, item: f"「{item}」快要過期，還不去看看？"
    },
    "pickup_reminder": {
        "subject": "食物領取提醒",
        "message": lambda user, item: f"提醒您，您預約的「{item}」即將到達領取時間。",
        "title": "⏰ 領取時間快到",
        "body": lambda user, item: f"您預約的「{item}」快到時間囉～"
    }
}


# ✅ 寄送 Gmail
def send_email(to_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = Header(subject, 'utf-8')
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# ✅ 發送 FCM 通知
def send_fcm(token, title, body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            token=token
        )
        response = messaging.send(message)
        print(f"✅ FCM sent: {response}")
    except Exception as e:
        print(f"❌ Failed to send FCM: {e}")


# ✅ 整合主函式：同時發送 Email 與 FCM
def notify_user(event_type, user_name, item_name, email, fcm_token):
    if event_type not in NOTIFICATION_TEMPLATES:
        print("❌ 不支援的事件類型")
        return

    template = NOTIFICATION_TEMPLATES[event_type]

    subject = template["subject"]
    message = template["message"](user_name, item_name)
    title = template["title"]
    body = template["body"](user_name, item_name)

    if email:
        send_email(email, subject, message)
    if fcm_token:
        send_fcm(fcm_token, title, body)
