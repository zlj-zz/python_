# coding:utf-8

import redis


class Config(object):
    """settings"""
    SECRET_KEY = 'ADJKL*8Iika*yAY568'
    # mysql setting
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # redis setting
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # flask-session setting
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # hide cookie's session id
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7


class DevelopmentConfig(Config):
    """development mode setting"""
    DEBUG = True


class ProductionConfig(Config):
    """product mode setting"""
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig,
}
