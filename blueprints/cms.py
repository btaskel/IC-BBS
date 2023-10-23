import logging
from datetime import datetime, timedelta

import psutil
from flask import Blueprint, render_template, current_app, request, g, redirect, url_for, flash

from exts import db, csrf
from forms.advert import AdvertForm
from forms.cms import WorkForm, BoardEditForm
from hooks import permission_required
from models.advert import AdvertModel
from models.event import WorkModel, ReportModel
from models.event import WorkTypeEnum
from models.posts import PostModel, BoardModel
from models.users import PermissionEnum, UserModel, RoleModel
from utils import restful
from utils.func.cms import recent_count, time_count

bp = Blueprint('cms', __name__, url_prefix='/cms')


# @bp.before_request
# def cms_before_request():
#     if not hasattr(g, 'user') or g.user.is_staff == False:
#         return redirect(url_for('front.index'))


@bp.get('/')
@permission_required(PermissionEnum.CMS_USER)
def cms_index():
    """
    内容管理系统主页
    :return:
    """
    logging.debug(f'User {g.user.username} visited the CMS homepage')
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)
    posts = PostModel.query.all()
    posts_7 = time_count(PostModel)
    users = UserModel.query.all()
    users_7 = time_count(UserModel)
    reports = ReportModel.query.all()
    reports_7 = time_count(ReportModel)
    workOrder_7 = time_count(WorkModel)

    user_list = recent_count(UserModel)
    post_list = recent_count(PostModel)
    report_list = recent_count(ReportModel)

    advert_list = recent_count(AdvertModel)

    storage = current_app.config['STORAGE']

    var = {
        'posts': posts,
        'posts_7': posts_7,
        'users': users,
        'users_7': users_7,
        'reports': reports,
        'reports_7': reports_7,
        'storage': storage,
        'user_list': user_list,
        'post_list': post_list,
        'report_list': report_list,

        'workOrder_7': workOrder_7,

        'adverts': advert_list,

        'cpu_percent': psutil.cpu_percent(interval=0.1),
        'mem_usage': psutil.virtual_memory().percent,
    }
    return render_template('cms/tabler/demo/home/home.html', var=var, user=g.user)


@bp.get('/home_info')
@permission_required(PermissionEnum.FRONT_USER)
def home_info():
    model_name = request.args.get('model')
    days = request.args.get('days')

    if isinstance(days, int):
        if days > 30 or days < 1:
            return restful.params_error('获取的日期超过范围')

    elif days.lower() == 'all':
        pass

    else:
        return restful.params_error('获取的日期的格式不正确')

    match model_name.lower():
        case 'report':
            model = ReportModel
        case 'post':
            model = PostModel
        case 'user':
            model = UserModel
        case 'work':
            model = WorkModel
        case _:
            return restful.server_error('没有找到对应模型')

    return restful.ok({
        'result': recent_count(model, days=days)
    })


@bp.route('/work_order', methods=['GET', 'POST'])
@csrf.exempt
@permission_required(PermissionEnum.FRONT_USER)
def work_order():
    """
    工单管理
    :return:
    """
    if request.method == 'GET':
        logging.debug(f'User {g.user.username} visited the CMS work_order')
        return render_template('cms/tabler/demo/work/pubic_work_order.html', WorkTypeEnum=WorkTypeEnum, user=g.user)

    elif request.method == 'POST':
        form = WorkForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            level = form.level.data
            report = WorkModel(title=title, content=content, level=level, user=g.user)
            db.session.add(report)
            db.session.commit()
            return redirect(url_for('cms.work_order'))
        else:
            flash('格式验证错误，创建工单失败')
            return redirect(url_for('cms.work_order'))


@bp.route('/work_index')
@permission_required(PermissionEnum.FRONT_USER)
def work_index():
    """
    待完成的工单
    :return:
    """

    """
    r1 = session.query(Users).all()
    r2 = session.query(Users.name.label('xx'), Users.age).all()
    r3 = session.query(Users).filter(Users.name == "alex").all()
    r4 = session.query(Users).filter_by(name='alex').all()
    r5 = session.query(Users).filter_by(name='alex').first()
    r6 = session.query(Users).filter(text("id<:value and name=:name")).params(value=224, name='fred').order_by(Users.id).all()
    r7 = session.query(Users).from_statement(text("SELECT * FROM users where name=:name")).params(name='ed').all()
    """
    logging.debug(f'User {g.user.username} visited the CMS work_index')

    # work_list = WorkModel.query.filter_by(active=True
    # print(work_list)
    return render_template('cms/tabler/demo/work/work_order.html', user=g.user)


@bp.route('/complete_work_order')
@permission_required(PermissionEnum.FRONT_USER)
def complete_work_order():
    """
    完成的工单清单
    """
    logging.debug(f'User {g.user.username} visited the CMS complete_work_order')
    ls = []
    works = WorkModel.query.all()
    for work in works:
        if work.finish:
            ls.append(work)
    return render_template("cms/tabler/demo/work/complete_work_order.html", works=ls, user=g.user)


@bp.route('/unfinished_work_order')
@permission_required(PermissionEnum.FRONT_USER)
def unfinished_work_order():
    """
    未完成的工单清单
    """
    logging.debug(f'User {g.user.username} visited the CMS unfinished_work_order')

    works = WorkModel.query.all()
    user = g.user
    return render_template("cms/tabler/demo/work/unfinished_work_order.html", works=works, user=user)


@bp.route('timeout_work_order')
@permission_required(PermissionEnum.FRONT_USER)
def timeout_work_order():
    """超时的工单清单"""
    logging.debug(f'User {g.user.username} visited the CMS timeout_work_order')

    works = WorkModel.query.all()
    user = g.user
    return render_template("cms/tabler/demo/work/timeout_work_order.html", works=works, user=user)


@bp.route('train')
@permission_required(PermissionEnum.FRONT_USER)
def train():
    """工单回收站"""
    logging.debug(f'User {g.user.username} visited the CMS timeout_work_order')

    works = WorkModel.query.all()
    user = g.user
    return render_template("cms/tabler/demo/work/train_order_work.html", works=works, user=user)


# @bp.route('/search_user', methods=['GET', 'POST'])
# @csrf.exempt
# @permission_required(PermissionEnum.FRONT_USER)
# def search_user():
#     if request.method == 'GET':
#         logging.debug(f'User {g.user.username} visited the CMS search_user')
#
#         return render_template('cms/tabler/demo/search.html')
#
#     elif request.method == 'POST':
#         user_id = request.args.get('user_id')
#         user_name = request.args.get('user_name')
#         if user_id:
#             user = UserModel.query.get(user_id)
#         else:
#             user = UserModel.query.filter_by(user_name=user_name)
#
#         return render_template('cms/tabler/demo/users.html', user=user)


# @bp.route('/post_index', methods=['GET'])
# @bp.route('/post_index/<int:post_id>', methods=['POST'])
@bp.get('/post_index')
@permission_required(PermissionEnum.FRONT_USER)
def post_index():
    logging.debug(f'User {g.user.username} visited the CMS post_index')

    if request.method == 'GET':
        user = g.user
        posts = PostModel.query.all()
        return render_template("cms/tabler/demo/post/posts_index.html", user=user, posts=posts)


@bp.post("/post_index/<int:post_id>")
@csrf.exempt
@permission_required(PermissionEnum.FRONT_USER)
def ban_post(post_id):
    logging.debug(f'User {g.user.username} visited the CMS ban_post')

    post = PostModel.query.get(post_id)
    if post:
        post.active = False
        db.session.commit()
    return redirect(url_for("cms.post_index"))


@bp.get('/ban_posts')
@permission_required(PermissionEnum.FRONT_USER)
def ban_posts():
    """封禁帖子"""
    logging.debug(f'User {g.user.username} visited the CMS ban_posts')

    user = g.user
    posts = PostModel.query.all()
    return render_template("cms/tabler/demo/post/ban_posts.html", user=user, posts=posts)


@bp.post('/ban_posts/<int:post_id>')
@csrf.exempt
@permission_required(PermissionEnum.FRONT_USER)
def restore_post(post_id):
    """解封帖子"""
    logging.debug(f'User {g.user.username} visited the CMS restore_post')

    post = PostModel.query.get(post_id)
    if post:
        post.active = True
        db.session.commit()
        flash(f"解封{post_id}成功")
    return restful.ok(f"解封{post_id}成功")


@bp.get('/reports_index')
@permission_required(PermissionEnum.FRONT_USER)
def reports_index():
    """举报列表：列出所有举报"""
    logging.debug(f'User {g.user.username} visited the CMS reports_index')

    reports = ReportModel.query.all()
    return render_template("cms/tabler/demo/report/reports_index.html", user=g.user, reports=reports)


@bp.post('/ban_report/<int:report_id>')
@permission_required(PermissionEnum.FRONT_USER)
def ban_report(report_id):
    """举报列表：将举报对象关闭活动"""
    logging.debug(f'User {g.user.username} visited the CMS ban_report')

    report = ReportModel.query.get(report_id)
    if report:
        report.active = False
        db.session.commit()
        flash(f'举报id：{report_id}已标记为停止活动')
    return redirect(url_for('cms.reports_index'))


@bp.route('/reported_resolved', methods=['GET', 'POST'])
@csrf.exempt
@permission_required(PermissionEnum.FRONT_USER)
def reported_resolved():
    """
    已解决的举报：获取被封禁的举报列表
    :return:
    """
    logging.debug(f'User {g.user.username} visited the CMS reported_resolved')

    if request.method == 'GET':
        reports = ReportModel.query.all()
        return render_template("cms/tabler/demo/report/reported_resolved.html", user=g.user, reports=reports)
    else:
        # 已解决的举报：恢复举报
        report_id = request.form.get('report_id')
        if report_id:
            report = ReportModel.query.get(report_id)
            if report:
                report.active = True
                db.session.commit()
                flash(f'举报id：{report_id}已标记为活动')
        return redirect(url_for('cms.reported_resolved'))


@bp.route('/report_bat', methods=['GET', 'POST'])
@csrf.exempt
@permission_required(PermissionEnum.FRONT_USER)
def report_bat():
    logging.debug(f'User {g.user.username} visited the CMS report_bat')

    """举报批量处理：批量处理界面"""
    if request.method == 'GET':
        reports = ReportModel.query.all()
        return render_template("cms/tabler/demo/report/report_bat.html", user=g.user, reports=reports)
    else:
        # todo: 批量处理举报
        return redirect(url_for('cms.report_bat'))


@bp.get('/user_index')
@permission_required(PermissionEnum.FRONT_USER)
def users_index():
    logging.debug(f'User {g.user.username} visited the CMS users_index')

    """用户列表：获取所有用户"""
    users = UserModel.query.all()
    return render_template("cms/tabler/demo/user/users_index.html", users=users, user=g.user)


@bp.post('/ban_user/<string:user_id>')
@csrf.exempt
@permission_required(PermissionEnum.FRONT_USER)
def ban_user(user_id):
    """用户列表：封禁用户"""
    logging.debug(f'User {g.user.username} visited the CMS ban_user')

    user = UserModel.query.get(user_id)
    if user:
        user.active = False
    return redirect(url_for('cms.users_index'))


@bp.get('/restore_user')
@permission_required(PermissionEnum.CMS_USER)
def restore_user_index():
    """封禁的用户：获取被封禁的用户"""
    logging.debug(f'User {g.user.username} visited the CMS restore_user_index')
    users = UserModel.query.all()
    return render_template("cms/tabler/demo/user/ban_users.html", users=users, user=g.user)


@bp.post('/restore_user/<string:user_id>')
@csrf.exempt
def restore_user(user_id):
    """封禁的举报：恢复举报"""
    logging.debug(f'User {g.user.username} visited the CMS restore_user')
    user = UserModel.query.get(user_id)
    if user:
        user.active = True
        db.session.commit()
    return flash(f'用户id：{user_id}已标记为活动')


@bp.get('/custom_permissions')
@permission_required(PermissionEnum.CMS_USER)
def custom_permissions():
    """自定义用户权限"""
    logging.debug(f'User {g.user.username} visited the CMS custom_permissions')
    user = g.user
    roles = RoleModel.query.all()
    return render_template("cms/tabler/demo/user/custom_permissions.html", user=user, roles=roles)


@bp.post('/custom_user_permission')
@permission_required(PermissionEnum.CMS_USER)
def custom_user_permission():
    """自定义用户权限"""
    logging.debug(f'User {g.user.username} visited the CMS custom_user_permission')
    user_id = request.args.get('user_id')
    role_id = request.args.get('role_id')

    user = UserModel.query.get(user_id)
    role = RoleModel.query.get(role_id)
    if user and role:
        user.role_id = role_id
        db.session.commit()
        return restful.ok()
    else:
        flash("错误：用户不存在或职位角色不存在！")
        return restful.params_error()


@bp.route('/board_manage', methods=['GET', 'POST'])
@csrf.exempt
@permission_required(PermissionEnum.CMS_USER)
def board_manage():
    """
    GET：获取板块静态管理界面
    POST：提交修改板块内容
    :return:
    """
    logging.debug(f'User {g.user.username} visited the CMS board_manage')
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('cms/tabler/demo/board/boards_index.html', user=g.user, boards=boards)
    else:
        method = request.form.get('btn')
        form = BoardEditForm(request.form)
        if form.validate():
            board_id = form.board_id.data
            board_name = form.board_name.data

            if method == 'edit':
                board = BoardModel.query.get(board_id)
                if board:
                    board.name = board_name
                    db.session.add(board)
                    db.session.commit()
                    flash(f'修改板块名称为：{board_name} 成功')
                else:
                    board = BoardModel(name=board_name)
                    db.session.add(board)
                    db.session.commit()
                    flash(f'添加板块{board.name}成功')

            elif method == 'delete':
                board = BoardModel.query.get(board_id)
                db.session.delete(board)
                db.session.commit()
                flash(f'删除板块{board_name}成功')
        return redirect(url_for('cms.board_manage'))


@bp.route('/advert_manage', methods=['GET', 'POST'])
@csrf.exempt
@permission_required(PermissionEnum.CMS_USER)
def advert_manage():
    """推广管理"""
    if request.method == 'GET':
        adverts = AdvertModel.query.all()
        return render_template('cms/tabler/demo/advert/advert_index.html', adverts=adverts, user=g.user)
    else:
        form = AdvertForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            post = form.post_url.data
            advert = AdvertModel(title=title, content=content, post=post)
            db.session.add(advert)
            db.session.commit()
        else:
            flash('推广增加失败！格式错误.')
            return redirect(url_for('cms.cms_index'))


@bp.post('/advert_delete')
@csrf.exempt
@permission_required(PermissionEnum.CMS_USER)
def advert_delete():
    advert_id = request.form.get('advert_id')
    if advert_id:
        advert = AdvertModel.query.get(advert_id)
        if advert:
            db.session.delete(advert)
            db.session.commit()