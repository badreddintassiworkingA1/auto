import smtplib
import imapclient
import email
import time
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# إعدادات حساب Yahoo
YAHOO_SMTP_SERVER = "smtp.mail.yahoo.com"
YAHOO_SMTP_PORT = 587
YAHOO_IMAP_SERVER = "imap.mail.yahoo.com"
EMAIL_ADDRESS = "axmrqpdaf@yahoo.com"  # ضع هنا بريدك
EMAIL_PASSWORD = "yLaT2wOhd0"  # ضع هنا الـ App Password من Yahoo

# قائمة ردود عشوائية لتجنب كشفك كـ سبام
responses = [
    "Hi, thanks for reaching out! Can you provide more details?",
    "Sounds interesting! What are the next steps?",
    "I appreciate the update. Let’s discuss this further.",
    "Great! I'm looking forward to more details."
]

def send_email(to_email, subject):
    """إرسال رد تلقائي عبر Yahoo SMTP"""
    body = random.choice(responses)  # اختيار رد عشوائي
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = f"Re: {subject}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(YAHOO_SMTP_SERVER, YAHOO_SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        print(f"✅ تم إرسال الرد إلى {to_email}")
    except Exception as e:
        print(f"❌ فشل إرسال الرد: {e}")

def read_and_reply():
    """قراءة البريد الوارد والرد عليه تلقائيًا"""
    try:
        # الاتصال بـ IMAP
        mail = imapclient.IMAPClient(YAHOO_IMAP_SERVER, ssl=True)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select_folder('INBOX')

        # البحث عن الرسائل غير المقروءة
        messages = mail.search(['UNSEEN'])

        for msg_id in messages:
            raw_message = mail.fetch(msg_id, ['RFC822'])[msg_id][b'RFC822']
            msg = email.message_from_bytes(raw_message)

            from_email = email.utils.parseaddr(msg['From'])[1]
            subject = msg['Subject'] if msg['Subject'] else "No Subject"

            print(f"📩 رسالة جديدة من {from_email} بعنوان: {subject}")

            # إرسال رد تلقائي
            send_email(from_email, subject)

            # وضع علامة "مقروء"
            mail.set_flags(msg_id, [imapclient.SEEN])

        mail.logout()
    except Exception as e:
        print(f"❌ خطأ أثناء قراءة البريد: {e}")

# تشغيل السكريبت كل 5 دقائق
while True:
    read_and_reply()
    time.sleep(300)  # 300 ثانية = 5 دقائق
