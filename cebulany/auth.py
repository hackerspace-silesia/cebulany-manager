from flask import request, current_app as app, abort
from functools import wraps


def token_required(view):

    @wraps(view)
    def inner(*args, **kwargs):
        header = request.headers.get('Authorization', '')
        token = app.config['CEBULANY_TOKEN']
        if header != 'Socek %s' % token:
            abort(401)
        view(*args, **kwargs)

    return inner
