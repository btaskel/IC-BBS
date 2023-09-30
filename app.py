from flask import Flask

import commands
import config
import hooks
from blueprints.cms import bp as cms_bp
from blueprints.event import bp as event_bp
from blueprints.front import bp as front_bp
from blueprints.post import bp as post_bp
from blueprints.user import bp as user_bp
from blueprints.bulletin import bp as bulletin_bp
from blueprints.test import bp as test_bp
from exts import db, Migrate, cache, scheduler
from exts import mail

app = Flask(__name__)

# 读取配置信息
app.config.from_object(config.ProductionConfig)

# 绑定对象到app
db.init_app(app)
cache.init_app(app)
mail.init_app(app)
scheduler.init_app(app)


migrate = Migrate(app, db)

# 添加钩子函数
app.before_request(hooks.bbs_before_request)

# 注册蓝图
app.register_blueprint(bulletin_bp)
app.register_blueprint(cms_bp)
app.register_blueprint(user_bp)
app.register_blueprint(post_bp)
app.register_blueprint(front_bp)
app.register_blueprint(event_bp)
app.register_blueprint(test_bp)

# 注册命令
app.cli.command('create_permission')(commands.create_permission)
app.cli.command('create_role')(commands.create_role)
app.cli.command('create_board')(commands.create_board)
app.cli.command('create_posts')(commands.create_posts)

if __name__ == '__main__':
    app.run(debug=True)
