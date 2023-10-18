from flask import Blueprint, g

from exts import db
from models.event import ReportModel, ReportTypeEnum
from models.event import WorkModel, WorkTypeEnum
from models.posts import PostModel
from models.users import UserModel

bp = Blueprint('test', __name__, url_prefix='/test')


@bp.route('/')
def test1():
    # student = Student.query.filter_by(name='Askel')
    # course = Course.query.filter_by(name='alpha')
    # print(student[0])
    # course = course[0]
    # student = student[0]
    #
    # student.courses.append(course)
    # db.session.add(student)
    # db.session.commit()
    user = UserModel.query.get("hL6AmpMsAu4wqonaDShW5K")
    print(user)
    works = WorkModel(title='Test', content='testContent', level=WorkTypeEnum.HIGH, user=user)
    db.session.add(works)
    db.session.commit()

    return 'ok'


@bp.route('/addreport')
def addre():
    user = UserModel.query.get('hL6AmpMsAu4wqonaDShW5K')
    post = PostModel.query.get(3)
    report = ReportModel(title='Title_', content='abc', user=user, report_type=ReportTypeEnum.name_calling, post=post)
    print(report)
    db.session.add(report)
    db.session.commit()
    return 'ok'


