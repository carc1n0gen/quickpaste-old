from flask.views import View
from pygments.formatters.img import JpgImageFormatter
from pygments.styles.native import NativeStyle
from app.repositories import paste
from app.helpers import abort_if
from app.util import highlight


class QuickPasteStyle(NativeStyle):
    background_color = 'rgb(63, 63, 70)'


class SocialBanner(View):
    methods = ['GET']

    def generate_social_image(self, doc, extension):
        return highlight(
            doc['text'],
            extension,
            JpgImageFormatter,
            # hl_lines=highlighted # TODO: revisit highlighing in the images
            style=QuickPasteStyle,
            line_pad=10,
            line_number_bg='rgb(63, 63, 70)',
            line_number_fg='#6f6f6f',
            line_number_pad=20,
            font_size=32
        )

    def dispatch_request(self, id, extension=None):
        doc = paste.get_paste(id)
        abort_if(doc is None, 404)
        return self.generate_social_image(doc, extension), {'Content-Type': 'image/jpeg'}
