import datetime

from exts import scheduler
from models.event import WorkModel


@scheduler.task('interval', id='check_work_order_timeout', seconds=3600)
def check_timeout():
    """
    定期检查工单超时
    """
    works = WorkModel.query.all()

    for work in works:
        term = work.end_time - work.create_time
        time = datetime.datetime.now() - term
        if time > work.create_time:
            work.timeout = True
    print('超时工单清理完成')
    return
