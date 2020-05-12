from flask import Blueprint, current_app, request, abort, url_for
from app.repositories import paste
from app.util import templated, text_or_redirect, about_text

edit_bp = Blueprint('edit', __name__)


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
    {'name': 'Plain Text', 'ext': 'txt'},
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


@edit_bp.route('/', methods=['GET', 'POST'])
@templated()
@text_or_redirect
def edit():
    if request.method == 'POST':
        maxlength = current_app.config.get('MAX_PASTE_LENGTH')
        text = request.form.get('text')
        extension = request.form.get('extension')

        if text is None or text.strip() == '':
            abort(400)
        elif maxlength is not None and len(text) > maxlength:
            abort(413)

        id = paste.insert_paste(text)
        return dict(url=url_for('view.view', id=id, extension=extension, _external=True))

    clone = request.args.get('clone')
    if clone == 'about':
        text = about_text
    elif clone is not None:
        text = paste.get_paste(clone)[0]
    else:
        text = None
    return dict(
        text=text,
        hide_new=True,
        languages=LANGUAGES,
        lang=request.args.get('lang')
    )
