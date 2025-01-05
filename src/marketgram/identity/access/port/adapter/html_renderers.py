from jinja2 import Template

from marketgram.common.application.message_renderer import HtmlRenderer


class UserActivationHtmlRenderer(HtmlRenderer[str]):
    def make_html_content(self, template: Template, fields: str) -> str:
        link = '{}{}'.format(self._html_settings.activate_link, fields)

        return template.render(link=link)
    
    
class PasswordChangeHtmlRenderer(HtmlRenderer[str]):
    def make_html_content(self, template: Template, fields: str):
        link = '{}{}'.format(self._html_settings.password_change_link, fields)

        return template.render(link=link)