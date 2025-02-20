import requests
import re
from datetime import datetime
import pytz
from config import MAILGUN_API_KEY, MAILGUN_DOMAIN

def send_email(body, EMAIL_RECEIVER, EMAIL_TITLE, timeoffset):
    print("Sending email...")
    try:
        # 使用正则表达式清理body中的Markdown代码块标记
        cleaned_body = re.sub(r'```(?:html)?', '', body)  # 删除```和```html

        # 获取当前 UTC 时间
        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        
        # 根据时区偏移量创建时区并转换时间
        timezone_str = f'Etc/GMT{"+" if timeoffset < 0 else "-"}{abs(timeoffset)}'
        local_timezone = pytz.timezone(timezone_str)
        local_now = utc_now.astimezone(local_timezone)
        custom_date = local_now.strftime('%Y-%m-%d')

        # 配置邮件参数
        data = {
            "from": f"LifeSync-AI <mailgun@sandbox22e9a53242634811975ad167d530a727.mailgun.org>",
            "to": [EMAIL_RECEIVER],
            "subject": f"{EMAIL_TITLE} {custom_date}",
            "html": cleaned_body
        }

        # 发送邮件请求到 Mailgun API
        response = requests.post(
            f"https://api.mailgun.net/v3/sandbox22e9a53242634811975ad167d530a727.mailgun.org/messages",
            auth=("api", 931642462084806de236e5a5f96d255c-ac3d5f74-b3cf32f5),
            data=data
        )
        
        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")

    except Exception as e:
        print("An error occurred while sending the email:")
        print(e)
