# coding:utf-8

import redis
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from ihome.utils.commons import ReConverter

# mysql
db = SQLAlchemy()
# create redis connection object
redis_store = None

# log level
logging.basicConfig(level=logging.DEBUG)
# set log path , size , cap
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# log format
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# set log format
file_log_handler.setFormatter(formatter)
# add log recorder
logging.getLogger().addHandler(file_log_handler)


# factory mode
def create_app(confing_name):
    """
    create flask app object
    :param confing_name: str mode_name("develop", "product")
    :return:
    """
    app = Flask(__name__)
    config_class = config_map.get(confing_name)
    app.config.from_object(config_class)

    db.init_app(app)
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)
    # flask-session , use redis save session
    Session(app)
    # add csrf safe
    CSRFProtect(app)
    # 引用自定义转换器
    app.url_map.converters["re"] = ReConverter
    # register blueprint
    from ihome import api_1_0
    app.register_blueprint(blueprint=api_1_0.api, url_prefix="/api/v1.0")
    # register static file blueprint
    from ihome import web_html
    app.register_blueprint(blueprint=web_html.html)

    return app
