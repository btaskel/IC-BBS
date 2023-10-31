import logging

from flask import Blueprint, render_template, g

from models.advert import AdvertModel

bp = Blueprint('advert', __name__, url_prefix='/advert')


@bp.route('/', methods=['GET'])
def ad_index():
    if hasattr(g, 'user'):
        logging.debug(f'User {g.user.username} visited the Advert ad_index')
    ads = AdvertModel.query.all()
    return render_template('front/advertisement.html', ads=ads)
