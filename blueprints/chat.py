from flask import Blueprint, render_template, g, request

bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('front/chat/index.html', user=g.user)
    else:
        pass