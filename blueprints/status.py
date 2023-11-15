from flask import Blueprint, render_template

bp = Blueprint('status', __name__, url_prefix='/status')


@bp.get('/error_404')
def error_404():
    return render_template('error/404.html')


@bp.get('/error_403')
def error_403():
    return render_template('error/403.html')


@bp.get('/error_500')
def error_500():
    return render_template('error/500.html')
