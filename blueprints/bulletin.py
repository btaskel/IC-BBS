from flask import Blueprint, request, render_template

bp = Blueprint('bulletin', __name__, url_prefix='/bulletin')


@bp.get('/bulletin')
def bulletin():
    return 'ok'