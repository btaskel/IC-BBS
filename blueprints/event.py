import logging

from flask import render_template, Blueprint, request, g, flash, redirect, url_for

from exts import db
from forms.event import ReportForm
from models.event import ReportModel
from models.posts import PostModel

bp = Blueprint('event', __name__, url_prefix='/event')


@bp.route('/report/<int:post_id>', methods=['GET', 'POST'])
def post_report(post_id):
    g.user and logging.debug(f'User {g.user.username} visited the Event post_report')

    if request.method == 'GET':
        post = PostModel.query.get(post_id)
        # todo: 渲染举报界面
        return render_template('', post=post)
    else:
        form = ReportForm()
        if form.validate():
            title = form.title.data
            content = form.content.data
            report_type = form.content.data
            user = g.user
            report = ReportModel(title=title, content=content, report_type=report_type, user=user)
            db.session.add(report)
            db.session.commit()
            flash('举报提交成功')
        else:
            for message in form.messages:
                flash(message)
        return redirect(url_for('post.post_detail', post_id=post_id))

