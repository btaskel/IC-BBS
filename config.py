class BaseConfig:
    """基本配置"""

    SECRET_KEY = "qjfksnm1gds"
    # 设置数据库URL
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/bbs?charset=utf8mb4'
    # 设置存储最大空间（单位：MB）
    STORAGE = 8192
    BBS_NAME = '长春大学旅游学院校园论坛'


class ProductionConfig(BaseConfig):
    """生产服务器配置"""
    # 媒体文件存放路径
    UPLOAD_FOLDER = r'./media'

    # 缓存配置
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = '6379'
    # Redis登陆密码
    CACHE_REDIS_PASSWORD = "Asker"

    # 邮箱收发配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_USERNAME = "1548559058@qq.com"
    MAIL_PASSWORD = "irqacqoigrgmjfjh"
    MAIL_DEFAULT_SENDER = "1548559058@qq.com"
