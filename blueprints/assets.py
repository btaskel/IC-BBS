import os

from flask import Blueprint, current_app, make_response

from utils.restful import params_error

bp = Blueprint('assets', __name__, url_prefix='/assets')


@bp.get('/logo')
def get_logo():
    """获取Logo图标"""
    try:
        image_data = open(os.path.join(current_app.config['UPLOAD_FOLDER'], 'local\\config\\logo.png'),
                          "rb").read()
    except Exception as e:
        print(e)
        return params_error('logo文件获取失败')
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@bp.get('/bbs_name')
def bbs_name():
    print(current_app.config['BBS_NAME'])
    return current_app.config['BBS_NAME']