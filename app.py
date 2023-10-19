import logging

from flask import Flask

import commands
import config
import hooks
from blueprints.advert import bp as ad_bp
from blueprints.cms import bp as cms_bp
from blueprints.event import bp as event_bp
from blueprints.front import bp as front_bp
from blueprints.media import bp as media_bp
from blueprints.post import bp as post_bp
from blueprints.test import bp as test_bp
from blueprints.user import bp as user_bp
from exts import db, Migrate, cache, scheduler, csrf
from exts import mail
from shell import initLogging
# 初始化环境

logging.info('Initialization completed!')
initLogging()

app = Flask(__name__)
# 读取配置信息
app.config.from_object(config.ProductionConfig)

# 绑定对象到app
db.init_app(app)
cache.init_app(app)
mail.init_app(app)
scheduler.init_app(app)
csrf.init_app(app)

migrate = Migrate(app, db)

# 添加钩子函数
app.before_request(hooks.bbs_before_request)

# 注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(user_bp)
app.register_blueprint(post_bp)
app.register_blueprint(front_bp)
app.register_blueprint(event_bp)
app.register_blueprint(test_bp)
app.register_blueprint(media_bp)
app.register_blueprint(ad_bp)

# 注册命令
app.cli.command('create_permission')(commands.create_permission)
app.cli.command('create_role')(commands.create_role)
app.cli.command('create_board')(commands.create_board)
app.cli.command('create_posts')(commands.create_posts)
logging.info('Loading completed')

if __name__ == '__main__':
    app.run(debug=True)
