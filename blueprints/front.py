import logging

from flask import Blueprint, render_template, session, redirect, url_for, current_app, g

from hooks import permission_required

bp = Blueprint('front', __name__, url_prefix='/')


@bp.route('/')
def index():
    logging.debug(f'User {g.user.username} visited the Front index')

    if session.get('user_id'):
        return redirect(url_for('post.post_list'))
    else:
        return render_template('front/index.html', title=current_app.config.get('BBS_NAME'))