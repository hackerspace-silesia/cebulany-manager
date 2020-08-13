from datetime import datetime
from functools import wraps

from flask import request, current_app as app, abort

from cebulany.models import db, User


def token_required(view):

    @wraps(view)
    def inner(*args, **kwargs):
        header = request.headers.get('Authorization', '')
        auth_name, _, header_token = header.partition(' ')

        if auth_name != 'Socek':
            abort(401)

        user_id, _, token = header_token.partition(':')

        user = User.query.filter_by(
            id=user_id,
            token=token,
        ).first()

        if user is None:
            abort(401)

        if user.token_time.replace(tzinfo=None) < datetime.utcnow():
            abort(401)

        user.update_token_time()
        db.session.add(user)
        db.session.commit()

        return view(*args, **kwargs)

    return inner
