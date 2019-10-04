from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_alembic import Alembic

mail = Mail()
alembic = Alembic()
limiter = Limiter(key_func=get_remote_address)

about_text = """
# Quickpaste

A dead simple code sharing tool.


## Features

**Syntax highlighting**

There is automatic language detection, but sometimes it gets it wrong.  To
override the language, just add or edit a file extension to the url.

**Line highlighting**

Click on a line number to highlight and target that line with the # part of the
URL.  Click the same line number again to un-highlight/un-target. You can also
Shift+Click as many lines as you like to highlight but no target them.

**Does not totally break without JavaScript**

No JavaScript is required to use the basic features of pasting code, saving it,
copying the link to share and targetting lines. But Shift-Clicking to highlight 
lines without targetting will not work.


## FAQ

**Are the snippets stored forever?**

NO! They are deleted after one week(ish).

**Is the code available?**

[github project](https://github.com/carc1n0gen/quickpaste)

**Can I use quickpaste from my terminal?**

`cat file-name | curl -H "X-Respondwith: link" -X POST -d "text=$(</dev/stdin)" https://quickpaste.net/`

*Notice: The "X-Respondwith: link" is important. Otherwise you will get a
redirect response.*

You could even alias the curl part of that command:

`alias quickpaste="curl -H \"X-Respondwith: link\" -X POST -d \"text=\$(</dev/stdin)\" https://quickpaste.net/"`

To make it as simple as:

`cat file-name | quickpaste`
"""
