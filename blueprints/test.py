from flask import Blueprint, g, render_template

from exts import db
from models.event import ReportModel, ReportTypeEnum
from models.event import WorkModel, WorkTypeEnum
from models.posts import PostModel
from models.users import UserModel

bp = Blueprint('test', __name__, url_prefix='/test')


@bp.route('/')
def test1():
    return render_template('test.html')

@bp.route('/2')
def test2():
    return 'oka'