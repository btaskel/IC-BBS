from datetime import datetime, timedelta

from flask import Blueprint, render_template, current_app, request, g, redirect, url_for, flash

from exts import db
from forms.cms import WorkForm, BoardEditForm
from hooks import permission_required
from models.event import WorkModel, ReportModel
from models.event import WorkTypeEnum
from models.posts import PostModel, BoardModel
from models.users import PermissionEnum, UserModel, RoleModel
from utils import restful
from utils.func.cms import recent_count, week_count

bp = Blueprint('cms', __name__, url_prefix='/cms')


# @bp.before_request
# def cms_before_request():
#     if not hasattr(g, 'user') or g.user.is_staff == False:
#         return redirect(url_for('front.index'))


@bp.route('/')
@permission_required(PermissionEnum.CMS_USER)
def cms_index():
    """
    内容管理系统主页
    :return:
    """
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)
    posts = PostModel.query.all()
    posts_7 = week_count(PostModel)
    users = UserModel.query.all()
    users_7 = week_count(UserModel)

    user_list = recent_count(UserModel)
    post_list = recent_count(PostModel)

    storage = current_app.config['STORAGE']

    var = {
        'posts': posts,
        'posts_7': posts_7,
        'users': users,
        'users_7': users_7,
        'storage': storage,
        'user_list': user_list,
        'post_list': post_list
    }

    return render_template('cms/tabler/demo/home.html', var=var)


@bp.route('/work_order', methods=['GET', 'POST'])
@permission_required(PermissionEnum.FRONT_USER)
def work_order():
    """
    工单管理
    :return:
    """
    if request.method == 'GET':
        return render_template('cms/tabler/demo/sub/pubic_work_order.html', WorkTypeEnum=WorkTypeEnum)

    elif request.method == 'POST':
        form = WorkForm(request.form)
        print(request.form.get('title'))
        print(request.form.get('content'))
        print(request.form.get('level'))
        if form.validate():
            title = form.title.data
            content = form.content.data
            level = form.level.data
            print(title, content, level)
            print('Compute')
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

    # work_list = WorkModel.query.filter_by(active=True
    # print(work_list)
    user = g.user
    return render_template('cms/tabler/demo/work_order.html', user=user)


@bp.route('/complete_work_order')
@permission_required(PermissionEnum.FRONT_USER)
def complete_work_order():
    """
    完成的工单清单
    """
    ls = []
    works = WorkModel.query.all()
    for work in works:
        if work.finish:
            ls.append(work)
    return render_template("cms/tabler/demo/complete_work_order.html", works=ls)


@bp.route('/unfinished_work_order')
@permission_required(PermissionEnum.FRONT_USER)
def unfinished_work_order():
    """
    未完成的工单清单
    """
    works = WorkModel.query.all()
    user = g.user
    return render_template("cms/tabler/demo/unfinished_work_order.html", works=works, user=user)


@bp.route('timeout_work_order')
@permission_required(PermissionEnum.FRONT_USER)
def timeout_work_order():
    """超时的工单清单"""
    works = WorkModel.query.all()
    user = g.user
    return render_template("cms/tabler/demo/timeout_work_order.html", works=works, user=user)


@bp.route('train')
@permission_required(PermissionEnum.FRONT_USER)
def train():
    """工单回收站"""
    works = WorkModel.query.all()
    user = g.user
    return render_template("cms/tabler/demo/train_order_work.html", works=works, user=user)


@bp.route('/search_user', methods=['GET', 'POST'])
@permission_required(PermissionEnum.FRONT_USER)
def search_user():
    if request.method == 'GET':
        return render_template('cms/tabler/demo/search.html')

    elif request.method == 'POST':
        user_id = request.args.get('user_id')
        user_name = request.args.get('user_name')
        if user_id:
            user = UserModel.query.get(user_id)
        else:
            user = UserModel.query.filter_by(user_name=user_name)

        return render_template('cms/tabler/demo/users.html', user=user)


# @bp.route('/post_index', methods=['GET'])
# @bp.route('/post_index/<int:post_id>', methods=['POST'])
@bp.get('/post_index')
@permission_required(PermissionEnum.FRONT_USER)
def post_index():
    if request.method == 'GET':
        user = g.user
        posts = PostModel.query.all()
        return render_template("cms/tabler/demo/post/posts_index.html", user=user, posts=posts)


@bp.post("/post_index/<int:post_id>")
@permission_required(PermissionEnum.FRONT_USER)
def ban_post(post_id):
    post = PostModel.query.get(post_id)
    if post:
        post.active = False
        db.session.commit()
    return redirect(url_for("cms.post_index"))


@bp.get('/ban_posts')
@permission_required(PermissionEnum.FRONT_USER)
def ban_posts():
    """封禁帖子"""
    user = g.user
    posts = PostModel.query.all()
    return render_template("cms/tabler/demo/post/ban_posts.html", user=user, posts=posts)


@bp.post('/ban_posts/<int:post_id>')
@permission_required(PermissionEnum.FRONT_USER)
def restore_post(post_id):
    """解封帖子"""
    post = PostModel.query.get(post_id)
    if post:
        post.active = True
        db.session.commit()
        flash(f"解封{post_id}成功")
    return 'ok'


@bp.get('/reports_index')
@permission_required(PermissionEnum.FRONT_USER)
def reports_index():
    """举报列表：列出所有举报"""
    reports = ReportModel.query.all()
    return render_template("cms/tabler/demo/report/reports_index.html", user=g.user, reports=reports)


@bp.post('/ban_report/<int:report_id>')
@permission_required(PermissionEnum.FRONT_USER)
def ban_report(report_id):
    """举报列表：将举报对象关闭活动"""
    report = ReportModel.query.get(report_id)
    if report:
        report.active = False
        db.session.commit()
        flash(f'举报id：{report_id}已标记为停止活动')
    return redirect(url_for('cms.reports_index'))


@bp.route('/reported_resolved', methods=['GET', 'POST'])
@permission_required(PermissionEnum.FRONT_USER)
def reported_resolved():
    """
    已解决的举报：获取被封禁的举报列表
    :return:
    """
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
@permission_required(PermissionEnum.FRONT_USER)
def report_bat():
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
    """用户列表：获取所有用户"""
    users = UserModel.query.all()
    return render_template("cms/tabler/demo/user/users_index.html", users=users, user=g.user)


@bp.post('/ban_user/<string:user_id>')
@permission_required(PermissionEnum.FRONT_USER)
def ban_user(user_id):
    """用户列表：封禁用户"""
    user = UserModel.query.get(user_id)
    if user:
        user.active = False
    return redirect(url_for('cms.users_index'))


@bp.get('/restore_user')
@permission_required(PermissionEnum.FRONT_USER)
def restore_user_index():
    """封禁的用户：获取被封禁的用户"""
    users = UserModel.query.all()
    return render_template("cms/tabler/demo/user/ban_users.html", users=users, user=g.user)


@bp.post('/restore_user/<string:user_id>')
def restore_user(user_id):
    """封禁的举报：恢复举报"""
    user = UserModel.query.get(user_id)
    if user:
        user.active = True
        db.session.commit()
    return flash(f'用户id：{user_id}已标记为活动')


@bp.get('/custom_permissions')
@permission_required(PermissionEnum.CMS_USER)
def custom_permissions():
    """自定义用户权限"""
    user = g.user
    roles = RoleModel.query.all()
    return render_template("cms/tabler/demo/user/custom_permissions.html", user=user, roles=roles)


@bp.post('/custom_user_permission')
@permission_required(PermissionEnum.CMS_USER)
def custom_user_permission():
    """自定义用户权限"""
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
@permission_required(PermissionEnum.CMS_USER)
def board_manage():
    """
    GET：获取板块静态管理界面
    POST：提交修改板块内容
    :return:
    """
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

@bp.route('/system_log')
@permission_required(PermissionEnum.CMS_USER)
def system_log():
    return render_template('')