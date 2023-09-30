from datetime import timedelta, datetime

from sqlalchemy import and_


def recent_count(Model):
    """
    计数当前30天内的新内容添加数据
    :param Model:
    :return List:
    """
    now = datetime.now()
    list_ = []
    for i in range(30):
        time = now - timedelta(days=i)
        time_ago = now - timedelta(days=i + 1)
        user_number = len(
            Model.query.filter(and_(time_ago < Model.create_time, Model.create_time < time)).all())
        list_.append(user_number)
    list_.reverse()
    return list_


def week_count(Model):
    """
    计数当前7天内的新内容和添加的对象
    :param Model:
    :return Object:
    """

    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)
    data_7 = Model.query.filter(Model.create_time >= seven_days_ago).all()
    return data_7
