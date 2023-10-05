from flask import Blueprint, render_template, session, redirect, url_for

from hooks import permission_required

bp = Blueprint('front', __name__, url_prefix='/')


@bp.route('/')
def index():
    if session.get('user_id'):
        return redirect(url_for('post.post_list'))
    else:
        return render_template('front/index.html')