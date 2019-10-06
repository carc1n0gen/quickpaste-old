from pygments.formatters import HtmlFormatter
from pygments.lexers import MarkdownLexer
from flask import request, redirect
from flask.views import View


class BaseView(View):
    def __init__(self):
        super().__init__()
        self.html_formatter = HtmlFormatter()
        self.markdown_lexer = MarkdownLexer()

    def redirect_or_text(self, url, status=200, message=None):
        respond_with = request.headers.get('X-Respondwith')
        if (respond_with == 'link'):
            return (
                message or url,
                status,
                {'Content-type': 'text/plain; charset=utf-8'}
            )
        return redirect(url)
