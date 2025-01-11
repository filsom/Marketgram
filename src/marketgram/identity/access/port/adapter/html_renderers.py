from jinja2 import Environment, Template

from marketgram.common.application.message_renderer import HtmlRenderer, JwtHtmlSettings
    

class JwtTokenHtmlRenderer(HtmlRenderer[JwtHtmlSettings, str]):
    def __init__(
        self, 
        jinja: Environment, 
        html_settings: JwtHtmlSettings
    ):
        super().__init__(jinja, html_settings)

    def make_html_content(
        self, 
        template: Template, 
        fields: str
    ) -> str:
        link = '{}{}'.format(self._html_settings.link, fields)

        return template.render(link=link)