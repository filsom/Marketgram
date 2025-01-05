from jinja2 import Template

from marketgram.common.application.message_renderer import HtmlRenderer
from marketgram.identity.access.application.commands.forgot_password import PasswordChangeToken
from marketgram.identity.access.application.commands.user_registration import (
    ActivationToken
)


class UserActivationHtmlRenderer(
    HtmlRenderer[ActivationToken]
):
    def make_html_content(
        self, 
        template: Template, 
        fields: ActivationToken
    ) -> str:
        link = '{}{}'.format(
            self._html_settings.activate_link, 
            fields.value
        )
        return template.render(link=link)
    
    
class PasswordChangeHtmlRenderer(
    HtmlRenderer[PasswordChangeToken]
):
    def make_html_content(
        self, 
        template: Template, 
        fields: PasswordChangeToken
    ) -> str:
        link = '{}{}'.format(
            self._html_settings.password_change_link, 
            fields.value
        )

        return template.render(link=link)