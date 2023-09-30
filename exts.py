from flask_apscheduler import APScheduler
from flask_caching import Cache
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

migrate = Migrate()

cache = Cache()

mail = Mail()

scheduler = APScheduler()
