from flask import abort


def abort_if(condition, status_code):
    if condition:
        abort(status_code)
