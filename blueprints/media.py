import logging
import os

from flask import Blueprint, current_app, g

bp = Blueprint('media', __name__, url_prefix='/media')


@bp.route('/<path:filename>')
def media_file(filename):
    """获取反转的URL"""
    if g.user:
        logging.debug(f'User {g.user.username} visited the Media media_file')

    return os.path.join(
        current_app.config.get(current_app.config.get('UPLOAD_FOLDER'), 'upload\\post_image\\', filename))
