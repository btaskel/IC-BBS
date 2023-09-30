from functools import wraps

from flask import session, g, abort

from models.users import UserModel


def bbs_before_request():
    if 'user_id' in session:
        user_id = session.get('user_id')
        try:
            user = UserModel.query.get(user_id)
            # 修改g对象的user属性的user值
            setattr(g, 'user', user)
        except Exception as e:
            print(e)
            pass


def permission_required(permission):
    """
    判断用户是否登录且有权限访问CMS
    """

    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if hasattr(g, 'user') and g.user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                # 状态码返回
                return abort(403)

        return inner

    return outer


if __name__ == '__main__':
    pass

# def bbs_404_error(error):
#     return render_template('errors/404.html'), 404
#
#
# def bbs_401_error(error):
#     return render_template('errors/401.html'), 401
#
#
# def bbs_500_error(error):
#     return render_template('errors/500.html'), 500
