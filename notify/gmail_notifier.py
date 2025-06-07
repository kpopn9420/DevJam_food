import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

GMAIL_USER = 'be.happy.forever717@gmail.com'
GMAIL_PASS = 'paoajteekhhnvxxj'

# ✅ 實際寄信函式
def send_email(to_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email  # ✅ 修正這一行，不能用 Header 包住 Email address
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

# ✅ 類別化的通知模板系統
EMAIL_TEMPLATES = {
    "booking_created": {
        "subject": "預約已成立！",
        "message": lambda user, item: f"您好 {user}，您已成功預約「{item}」，請準時領取。"
    },
    "deal_completed": {
        "subject": "交易完成通知",
        "message": lambda user, item: f"您好 {user}，您與對方的「{item}」交易已完成，歡迎留下評價！"
    }
}

# ✅ 上層封裝用於主程式使用
def send_event_email(to_email, template_key, user_name, item_name):
    if template_key not in EMAIL_TEMPLATES:
        print("❌ 無此通知類型")
        return

    subject = EMAIL_TEMPLATES[template_key]["subject"]
    message = EMAIL_TEMPLATES[template_key]["message"](user_name, item_name)
    send_email(to_email, subject, message)
