import logging
import os
import re
from uuid import uuid4

from flask import Blueprint, render_template, request, g, redirect, url_for, flash, jsonify, current_app, make_response

from decorators import login_register
from exts import db, csrf
from forms.posts import CommentForm, PostForm
from models.posts import PostModel, CommentModel, BoardModel, PostImagesModel
from utils import restful

bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route('/')
def post_list():
    """返回首页信息"""
    logging.debug(f'User {g.user.username} visited the Post post_list')

    board_id = request.args.get('board')
    if board_id is None:
        posts = PostModel.query.all()
    else:
        board = BoardModel.query.get(board_id)
        if board:
            posts = board.posts
        else:
            posts = PostModel.query.all()
    boards = BoardModel.query.all()
    return render_template('front/post.html', posts=posts, boards=boards, user=g.user)


@bp.route('/post_detail/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    """帖子详情和评论提交"""
    logging.debug(f'User {g.user.username} visited the Post post_detail')

    boards = BoardModel.query.all()
    if request.method == 'GET':
        post = PostModel.query.get(post_id)
        if g.user:
            post.views += 1
            db.session.commit()
        return render_template('front/post_detail.html', post=post, boards=boards, user=g.user)
    else:
        form = CommentForm(request.form)
        if form.validate():
            content = form.content.data
            comment = CommentModel(content=content, post_id=post_id, author_id=g.user.id)
            db.session.add(comment)
            db.session.commit()
        else:
            for message in form.messages:
                flash(message)
        return redirect(url_for('post.post_detail', post_id=post_id, boards=boards))


@bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    """
    创建帖子
    get：返回编辑界面
    post：提交内容
    """
    logging.debug(f'User {g.user.username} visited the Post add_post')

    boards = BoardModel.query.all()
    if request.method == 'GET':
        return render_template('front/add_post.html', boards=boards, user=g.user)

    elif request.method == 'POST':
        content = re.sub('<img[^>]*>', '', request.form.get('content'))
        if len(content) > 4000:
            flash('文章内容不得超过4000字！')
            return redirect(url_for('post.post_list', boards=boards))
        form = PostForm(request.form)
        if form.validate():
            title = form.title.data
            board_id = form.board_id.data
            images = form.images.data

            try:
                images = images.split(',')
            except:
                return restful.params_error()
            post = PostModel(title=title, content=content, author=g.user, board_id=board_id)
            for image in images:
                if len(image) > 256:
                    return restful.params_error()
                try:
                    ext = image.split('.')[-1]
                    if ext not in ['jpg', 'png', 'gif', 'jpeg']:
                        return restful.params_error('不支持的图片格式')
                except:
                    return restful.params_error('上传的图片格式无法识别')
                if os.path.exists(image):
                    filename = os.path.basename(image)
                    image = PostImagesModel(name=filename, path=image)
                    db.session.add(image)
                    db.session.commit()
                    post.images.append(image)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('post.post_list', boards=boards))

        else:
            print('失败')
            flash('添加帖子时发生错误')
            return redirect(url_for('post.post_list', boards=boards))


# 装饰器执行是从里到外的
@bp.post('/upload/image')
@csrf.exempt
@login_register
def upload_image():
    # 判断后缀名是否符合要求
    logging.debug(f'User {g.user.username} visited the Post upload_image')
    f = next(iter(request.files.values()), None)
    try:
        extension = f.filename.split('.')[-1].lower()
    except:
        print('awdaw')
        return jsonify({
            'errno': 400,
            'data': []
        })

    if extension not in ['jpg', 'png', 'gif', 'jpeg']:
        return jsonify({
            'errno': 400,
            'data': []
        })
    # 将filename安全化
    # save_filename = str(uuid.uuid4()) + '.' + extension
    filename = str(uuid4()) + '.' + extension
    save_path = os.path.join(current_app.config.get('UPLOAD_FOLDER'), 'upload\\post_image\\' + filename)
    f.save(save_path)
    url = save_path
    return jsonify({
        'data': [{
            'url': url,
            'alt': '',
            'href': ''
        }]
    })


@bp.get('/show/<string:filename>')
@csrf.exempt
@login_register
def show_image(filename):
    logging.debug(f'User {g.user.username} visited the Post show_image')

    file_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'upload\\post_image\\')
    if filename is None:
        return redirect(url_for('post.post_list'))
    else:
        try:
            image_data = open(os.path.join(file_dir, filename), "rb").read()
        except:
            return redirect(url_for('post.post_list'))
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response


@bp.post('/remove_post/<string:post_id>')
@csrf.exempt
@login_register
def remove_post(post_id):
    """删除帖子"""
    logging.debug(f'User {g.user.username} visited the Post remove_post')

    user = g.user
    post = PostModel.query.get(post_id)
    if user.email == post.author.email:
        db.session.delete(post)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error()
