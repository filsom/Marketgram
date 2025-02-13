from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment


class HtmlRenderer:
    def __init__(
        self,
        sender: str,
        jinja_env: Environment,
    ) -> None:
        self._sender = sender
        self._jinja = jinja_env

    async def render(
        self, 
        template_name: str,
        subject: str,
        recipient: str, 
        fields: dict[str, str]
    ) -> MIMEMultipart:
        template = self._jinja.get_template(template_name)
        html_page = await template.render_async(fields)

        message = MIMEMultipart('alternative')
        message['From'] = self._sender
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(html_page, 'html'))

        return message