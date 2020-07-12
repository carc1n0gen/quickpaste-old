import functools
from pygments import highlight as pygment_highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_for_filename
from pygments.util import ClassNotFound
from flask import request, redirect
from flask_mail import Mail
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter


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


def highlight(text, extension=None):
    try:
        lexer = get_lexer_for_filename('foo.{}'.format(extension))
    except ClassNotFound:
        lexer = guess_lexer(text)

    return pygment_highlight(text, lexer, HtmlFormatter())
