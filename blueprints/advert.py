import logging

from flask import Blueprint, render_template, g

bp = Blueprint('advert', __name__, url_prefix='/advert')

@bp.route('/', methods=['GET'])
def ad_index():
    logging.debug(f'User {g.user.username} visited the Advert ad_index')
    return render_template('front/advertisement.html')