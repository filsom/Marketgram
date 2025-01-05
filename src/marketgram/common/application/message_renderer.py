from dataclasses import dataclass
from typing import Generic, TypeVar
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, Template


@dataclass
class ContentFields:
    pass


CF = TypeVar('CF', bound=ContentFields)


@dataclass
class HtmlSettings:
    sender: str
    subject: str
    activate_link: str
    password_change_link: str


class MessageRenderer(Generic[CF]):
    def render(self, recipient: str, fields: CF) -> MIMEMultipart:
        raise NotImplementedError


class HtmlRenderer(MessageRenderer[CF]):
    def __init__(
        self,
        template_name: str,
        jinja: Environment,
        html_settings: HtmlSettings
    ) -> None:
        self._template_name = template_name
        self._jinja = jinja
        self._html_settings = html_settings

    def render(self, recipient: str, fields: CF) -> MIMEMultipart:
        template = self._jinja.get_template(self._template_name)
        content = self.make_html_content(template, fields)

        message = MIMEMultipart('alternative')
        message['From'] = self._html_settings.sender
        message['To'] = recipient
        message['Subject'] = self._html_settings.subject
        message.attach(MIMEText(content, 'html'))

        return message

    def make_html_content(self, template: Template, fields: CF) -> str:
        raise NotImplementedError