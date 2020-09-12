
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

**CLI Script**

[Here is a cli script for creating pastes from the command line.](https://quickpaste.net/cli.py)

Note: only python 3.8 is tested.

Just download it, rename it to `quickpaste`, mark it as executable, and put it somewhere in the path.

## FAQ

**Are the snippets stored forever?**

NO! They are deleted after one week(ish).

**Is the code available?**

[github project](https://github.com/carc1n0gen/quickpaste)"""


cli_text = """#!/usr/bin/env python3
#
# Usage: cat <filename> | quickpaste [-l|--lang <lang>][-d|--delete-after <days>]
# (lang is the file extension for the language)
#

import os
import sys
from urllib import request, parse
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-l', '--lang', dest='lang', default='txt', help='the file extension for the language')
parser.add_option('-d', '--delete-after', dest='delete_after', default='7', help='Number of days until paste deletes (in days, between 1 - 7)')
(options, args) = parser.parse_args()

QUICKPASTE_HOST = os.getenv('QUICKPASTE_HOST', 'https://quickpaste.net')

with request.urlopen(QUICKPASTE_HOST) as response:
    cookie_string = response.headers['Set-Cookie']
    csrf_token = response.headers['CSRF_TOKEN']

text = ''
for line in sys.stdin:
    text = text + line

data = parse.urlencode({
    'csrf_token': csrf_token,
    'text': text,
    'extension': options.lang,
    'delete_after': options.delete_after
}).encode()

opener = request.build_opener()
opener.addheaders = [('Cookie', cookie_string), ('Accept', 'text/plain')]
with opener.open(QUICKPASTE_HOST, data=data) as response:
    print(response.read().decode('utf-8'))"""
