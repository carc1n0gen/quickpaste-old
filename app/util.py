import functools
import pymongo
from pygments import highlight as pygment_highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_for_filename
from pygments.util import ClassNotFound
from flask import request, redirect
from flask_mail import Mail
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from app.repositories import get_db

mail = Mail()
limiter = Limiter(key_func=get_remote_address)

LANGUAGES = [
    ('', 'auto-detect language'),
    ('ada', 'Ada'),
    ('sh', 'Bash'),
    ('c', 'C'),
    ('cs', 'C#'),
    ('cpp', 'C++'),
    ('clj', 'Clojure'),
    ('cljs', 'ClojureScript'),
    ('coffee', 'CoffeeScript'),
    ('cr', 'Crystal'),
    ('css', 'CSS'),
    ('d', 'D'),
    ('dart', 'Dart'),
    ('django', 'Django Template'),
    ('ex', 'Elixir'),
    ('erl', 'Erlang'),
    ('fs', 'F#'),
    ('fish', 'Fish'),
    ('f', 'Fortran'),
    ('go', 'Go'),
    ('groovy', 'Groovy'),
    ('haml', 'Haml'),
    ('hbs', 'Handlebars'),
    ('hs', 'Haskell'),
    ('html', 'HTML'),
    ('ini', 'INI'),
    ('java', 'Java'),
    ('jsp', 'Java Server Page'),
    ('js', 'JavaScript'),
    ('json', 'JSON'),
    ('jinja', 'Jinja Template'),
    ('kt', 'Kotlin'),
    ('less', 'Less'),
    ('liquid', 'Liquid Template'),
    ('lua', 'Lua'),
    ('md', 'Markdown'),
    ('moon', 'MoonScript'),
    ('nim', 'Nim'),
    ('m', 'Objective-C'),
    ('ml', 'OCaml'),
    ('pl', 'Perl'),
    ('php', 'PHP'),
    ('txt', 'Plain Text'),
    ('py', 'Python'),
    ('rb', 'Ruby'),
    ('rs', 'Rust'),
    ('scss', 'SASS'),
    ('sql', 'SQL'),
    ('swift', 'Swift'),
    ('toml', 'TOML'),
    ('twig', 'Twig Template'),
    ('ts', 'TypeScript'),
    ('vala', 'Vala'),
    ('xml', 'XML'),
    ('yaml', 'YAML', ),
]

about_text = """# Quickpaste

A dead simple code sharing tool.


## Features

**Syntax highlighting**

There is automatic language detection, but sometimes it gets it wrong.  To
override the language, just add or edit a file extension to the url.

**Line highlighting**

Click on a line number to highlight and target the line with the # part of the
URL. Control+Click (Command+Click on mac) a line to highlight it without
targeting it (This can be done to as many lines as you like).  Click on a
highlighted line to un-highlight it.

**Does not totally break without JavaScript**

No JavaScript is required to use the basic features of pasting code, saving it,
copying the link to share or targetting lines. But Shift-Clicking to highlight
lines without targetting, and un-highlighting lines (for example if someone
shared a link with you pre-highlighted) will not work.


## FAQ

**Are the snippets stored forever?**

NO! They are deleted after one week(ish).

**Is the code available?**

[github project](https://github.com/carc1n0gen/quickpaste)"""


def text_or_redirect(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            ctx = f(*args, **kwargs)
            if not isinstance(ctx, dict):
                return ctx

            accept = request.headers.get('Accept')
            status = ctx.get('status', 200)
            message = ctx.get('message')
            url = ctx.get('url')
            if accept == 'text/plain':
                if message:
                    text = message
                else:
                    text = url
                return text + '\n', status, {'Content-type': 'text/plain; charset=utf-8'}
            return redirect(url)

        return f(*args, **kwargs)
    return decorated_function


def configure_mongo(app):
    db = get_db()
    pastes = db['pastes']

    try:
        pastes.drop_index('paste_ttl')
    except pymongo.errors.OperationFailure:
        pass

    pastes.create_index('delete_at', expireAfterSeconds=0, name='paste_ttl')


def highlight(text, extension=None):
    try:
        lexer = get_lexer_for_filename('foo.{}'.format(extension))
    except ClassNotFound:
        lexer = guess_lexer(text)

    return pygment_highlight(text, lexer, HtmlFormatter())
