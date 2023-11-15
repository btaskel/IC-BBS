from flask import Blueprint, render_template, g
from decorators import login_register

bp = Blueprint('message', __name__, url_prefix='/message')


@bp.route('/index')
@login_register
def index():
    return render_template('front/messages.html', user=g.user)
