from flask import request, redirect
from flask.views import View


class BaseView(View):

    def redirect_or_text(self, url, status=200, message=None):
        respond_with = request.headers.get('X-Respondwith')
        if (respond_with == 'link'):
            return (
                message or url,
                status,
                {'Content-type': 'text/plain; charset=utf-8'}
            )
        return redirect(url)
