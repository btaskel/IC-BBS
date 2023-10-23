import os

import click

from exts import db
from models.posts import BoardModel, PostModel
from models.users import PermissionEnum, PermissionModel, RoleModel, UserModel


def create_permission():
    """用于创建权限表"""
    permission_list = []
    for permission_name in dir(PermissionEnum):
        if permission_name.startswith('__'):
            continue
        value = getattr(PermissionEnum, permission_name)
        permission_list.append(value)
        permission = PermissionModel(name=value)
        db.session.add(permission)
    db.session.commit()
    click.echo(f'增加权限：\n{permission_list}\n成功。')


# def create_report():
#     report_list = []
#     for report_name in dir()


def create_role():
    # 审查者
    inspector = RoleModel(name='审查', desc='负责适合帖子和评论是否合规')
    inspector.permissions = PermissionModel.query.filter(
        PermissionModel.name.in_([
            PermissionEnum.POST,
            PermissionEnum.COMMENT
        ])).all()

    # 运营者
    operator = RoleModel(name='运营', desc='负责网站持续正常运营')
    operator.permissions = PermissionModel.query.filter(PermissionModel.name.in_([
        PermissionEnum.POST,
        PermissionEnum.COMMENT,
        PermissionEnum.BOARD,
        PermissionEnum.FRONT_USER,
        PermissionEnum.CMS_USER
    ])).all()

    # 管理员
    administrator = RoleModel(name='管理员', desc='负责整个网站的所有工作')
    administrator.permissions = PermissionModel.query.all()

    db.session.add_all([inspector, operator, administrator])
    db.session.commit()
    click.echo('角色创建成功')


def create_board():
    board_names = ['学习交流','社团活动','日常灌水']
    for board_name in board_names:
        board = BoardModel(name=board_name)
        db.session.add(board)
    db.session.commit()
    click.echo('板块添加成功')


def create_posts():
    board = BoardModel.query.get(1)
    author = UserModel.query.get("SCZ2vKgByitGubsfH6Locc")
    post = PostModel(title='测试用文章', content='内容测试，内容测试，内容测试，内容测试，内容测试，内容测试，内容测试',
                     board=board, author=author)
    db.session.add(post)
    db.session.commit()
    click.echo('创建文章成功')

def clear_logs():
    path = 'logs\\'
    dirs = os.listdir(path)
    for file in dirs:
        if file.endswith('.log'):
            try:
                os.remove(os.path.join(path,file))
            except Exception as e:
                print(e)
                print('请等待服务器关闭后再清理日志')


if __name__ == '__main__':
    # create_permission()
    pass
