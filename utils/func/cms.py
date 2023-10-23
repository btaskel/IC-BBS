from datetime import timedelta, datetime

from sqlalchemy import and_


def recent_count(Model, days=30):
    """
    获取在days天内某一模型数量所增加的量
    :param days:
    :param Model:
    :return List:
    """
    now = datetime.now()
    list_ = []
    if days == 'all':
        return len(Model.query.all())

    for i in range(days):
        time = now - timedelta(days=i)
        time_ago = now - timedelta(days=i + 1)
        user_number = len(Model.query.filter(and_(time_ago < Model.create_time, Model.create_time < time)).all())
        list_.append(user_number)
    list_.reverse()

    if len(list_) < days:
        fill = days - len(list_)
        for i in range(fill):
            list_.append(0)
    print(list_)
    return list_


def time_count(Model, days=7):
    """
    :param Model:
    :param days:
    :return:
    """
    if days == 'all':
        return len(Model.query.all())
    now = datetime.now()
    time_ago = now - timedelta(days=days)
    return Model.query.filter(and_(Model.create_time > time_ago, now > Model.create_time)).all()
