import os

from flask import Blueprint, render_template, request, g, redirect, url_for, flash, jsonify, current_app
from werkzeug.utils import secure_filename

from exts import db
from forms.posts import CommentForm, PostForm
from models.posts import PostModel, CommentModel

bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route('/')
def post_list():
    """返回首页信息"""
    posts = PostModel.query.all()
    return render_template('front/post.html', posts=posts)


@bp.route('/post_detail/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    """帖子详情和评论提交"""
    if request.method == 'GET':
        post = PostModel.query.get(post_id)
        if g.user:
            post.views += 1
            db.session.commit()
        return render_template('front/post_detail.html', post=post)
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
        return redirect(url_for('post.post_detail', post_id=post_id))


@bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    """
    创建帖子
    get：返回编辑界面
    post：提交内容
    """
    if request.method == 'GET':
        return render_template('front/add_post.html')

    elif request.method == 'POST':
        form = PostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            post = PostModel(title=title, content=content, author=g.user, board_id=board_id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('post.post_list'))

        else:
            flash('添加帖子时发生错误')
            return redirect(url_for('post_list'))


@bp.post("/upload/image")
def upload_image():
    """上传图片视图函数"""
    f = request.files.get("image")
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return jsonify({
            "errno": 400,
            "data": []
        })
    filename = secure_filename(f.filename)
    f.save(os.path.join(current_app.config.get("UPLOAD_IMAGE_PATH"), filename))
    url = url_for('media.media_file', filename=filename)
    return jsonify({
        "errno": 0,
        "data": [{
            "url": url,
            "alt": "",
            "href": ""
        }]
    })
