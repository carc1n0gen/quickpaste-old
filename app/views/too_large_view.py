from pygments import highlight
from flask import render_template, current_app
from app.views import BaseView


class TooLargeView(BaseView):

    def dispatch_request(self, error):
        text = f"""
# Too many characters

Limit: {current_app.config['MAX_PASTE_LENGTH']}"""
        return render_template(
            'view.html',
            text=highlight(text, self.markdown_lexer, self.html_formatter),
            lines=text.count('\n') + 1,
            disabled=['clone', 'save', 'raw', 'download'],
        ), 413
