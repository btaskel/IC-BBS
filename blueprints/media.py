import os

from flask import Blueprint, current_app

bp = Blueprint('media', __name__, url_prefix='/media')


@bp.route('/<path:filename>')
def media_file(filename):
    """获取反转的URL"""
    return os.path.join(
        current_app.config.get(current_app.config.get('UPLOAD_FOLDER'), 'upload\\post_image\\', filename))
