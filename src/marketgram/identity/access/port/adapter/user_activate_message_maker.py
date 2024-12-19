from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from typing import Any


class UserActivateMessageMaker:
    def make(self, fields: Any, _for: str): 
        message = MIMEMultipart('alternative')

        message['From'] = ''
        message['To'] = _for
        message['Subject'] = 'Activate user'

        token = '{}{}'.format('http://127.0.0.1:8000/activate/', fields) 
        html_text = MIMEText(token)
        message.attach(html_text)

        return message
        