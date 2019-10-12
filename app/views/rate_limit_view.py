from pygments import highlight
from flask import render_template, current_app
from app.views import BaseView


class RateLimitView(BaseView):

    def dispatch_request(self, error):
        text = f"""
# Too Many Requests

**Limit: {current_app.config.get('RATELIMIT_DEFAULT')}**"""
        return render_template(
            'view.html',
            text=highlight(text, self.markdown_lexer, self.html_formatter),
            lines=text.count('\n') + 1
        ), 429
