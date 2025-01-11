from jinja2 import Template

from marketgram.common.application.message_renderer import HtmlRenderer
    

class JwtTokenHtmlRenderer(HtmlRenderer[str]):
    def make_html_content(
        self, 
        template: Template, 
        fields: str
    ) -> str:
        link = '{}{}'.format(self._html_settings, fields)

        return template.render(link=link)