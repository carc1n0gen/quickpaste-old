from pygments import highlight as pygment_highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename, TextLexer, _iter_lexerclasses
from pygments.util import ClassNotFound
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


def find_best_lexer(text, min_confidence=0.85):
    """
    Like the built in pygments guess_lexer, except has a minimum confidence
    level.  If that is not met, it falls back to plain text to avoid bad
    highlighting.

    :returns: Lexer instance
    """
    current_best_confidence = 0.0
    current_best_lexer = None
    for lexer in _iter_lexerclasses():
        confidence = lexer.analyse_text(text)
        if confidence == 1.0:
            return lexer()
        elif confidence > current_best_confidence:
            current_best_confidence = confidence
            current_best_lexer = lexer

    if current_best_confidence >= min_confidence:
        return current_best_lexer()
    else:
        return TextLexer()


def highlight(text, extension=None):
    try:
        lexer = get_lexer_for_filename('foo.{}'.format(extension))
    except ClassNotFound:
        lexer = find_best_lexer(text)

    return pygment_highlight(text, lexer, HtmlFormatter())
