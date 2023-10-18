from flask import Blueprint, render_template

bp = Blueprint('advert', __name__, url_prefix='/advert')

@bp.route('/', methods=['GET'])
def ad_index():
    return render_template('front/advertisement.html')