from functools import wraps

from flask import g, render_template, redirect, url_for


def login_register(func):

    @wraps(func)
    def inner(*args, **kwargs):
        if not hasattr(g, 'user') and not g.user.is_active:
            return redirect(url_for('user.login'))
        else:
            return func(*args, **kwargs)
    return inner