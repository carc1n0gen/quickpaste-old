from flask import request, current_app, url_for, render_template, abort
from app.views import BaseView
from app.shortlink import shortlink
import app.repositories.paste as paste

LANGUAGES = [
    {'name': 'Ada', 'ext': 'ada'},
    {'name': 'Bash', 'ext': 'sh'},
    {'name': 'C', 'ext': 'c'},
    {'name': 'C#', 'ext': 'cs'},
    {'name': 'C++', 'ext': 'cpp'},
    {'name': 'Clojure', 'ext': 'clj'},
    {'name': 'ClojureScript', 'ext': 'cljs'},
    {'name': 'CoffeeScript', 'ext': 'coffee'},
    {'name': 'Crystal', 'ext': 'cr'},
    {'name': 'CSS', 'ext': 'css'},
    {'name': 'D', 'ext': 'd'},
    {'name': 'ClojureScript', 'ext': 'cljs'},
    {'name': 'Dart', 'ext': 'dart'},
    {'name': 'Django Template', 'ext': 'django'},
    {'name': 'Elixir', 'ext': 'ex'},
    {'name': 'Erlang', 'ext': 'erl'},
    {'name': 'F#', 'ext': 'fs'},
    {'name': 'Fish', 'ext': 'fish'},
    {'name': 'Fortran', 'ext': 'f'},
    {'name': 'Go', 'ext': 'go'},
    {'name': 'Groovy', 'ext': 'groovy'},
    {'name': 'Haml', 'ext': 'haml'},
    {'name': 'Handlebars', 'ext': 'hbs'},
    {'name': 'Haskell', 'ext': 'hs'},
    {'name': 'HTML', 'ext': 'html'},
    {'name': 'INI', 'ext': 'ini'},
    {'name': 'Elixir', 'ext': 'ex'},
    {'name': 'Java', 'ext': 'java'},
    {'name': 'Java Server Page', 'ext': 'jsp'},
    {'name': 'JavaScript', 'ext': 'js'},
    {'name': 'JSON', 'ext': 'json'},
    {'name': 'Jinja Template', 'ext': 'jinja'},
    {'name': 'Kotlin', 'ext': 'kt'},
    {'name': 'Less', 'ext': 'less'},
    {'name': 'Liquid Template', 'ext': 'liquid'},
    {'name': 'Lua', 'ext': 'lua'},
    {'name': 'Markdown', 'ext': 'md'},
    {'name': 'MoonScript', 'ext': 'moon'},
    {'name': 'Nim', 'ext': 'nim'},
    {'name': 'Objective-C', 'ext': 'm'},
    {'name': 'OCaml', 'ext': 'ml'},
    {'name': 'Perl', 'ext': 'pl'},
    {'name': 'PHP', 'ext': 'php'},
    {'name': 'Python', 'ext': 'py'},
    {'name': 'Ruby', 'ext': 'rb'},
    {'name': 'Rust', 'ext': 'rs'},
    {'name': 'SASS', 'ext': 'scss'},
    {'name': 'SQL', 'ext': 'sql'},
    {'name': 'Swift', 'ext': 'swift'},
    {'name': 'TOML', 'ext': 'toml'},
    {'name': 'Twig Template', 'ext': 'twig'},
    {'name': 'TypeScript', 'ext': 'ts'},
    {'name': 'Vala', 'ext': 'vala'},
    {'name': 'XML', 'ext': 'xml'},
    {'name': 'YAML', 'ext': 'yaml'},
]


class EditView(BaseView):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            maxlength = current_app.config.get('MAX_PASTE_LENGTH')
            text = request.form.get('text')
            extension = request.form.get('extension')

            if text is None or text.strip() == '':
                abort(400)
            elif maxlength is not None and len(text) > maxlength:
                abort(413)

            id = paste.insert_paste(text)
            sh = shortlink.encode(id)
            if extension:
                url = url_for(
                    'paste.view.extension',
                    id=sh,
                    extension=extension,
                    _external=True
                )
            else:
                url = url_for('paste.view', id=sh, _external=True)
            return self.redirect_or_text(url, 200)

        text, _ = paste.get_paste(shortlink.decode(request.args.get('clone')))
        lang = request.args.get('lang')
        return render_template(
            'index.html',
            text=text,
            hide_new=True,
            languages=LANGUAGES,
            lang=lang,
        )
