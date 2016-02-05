#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os

#basedir为zhuxiang.py即当前文件所在的目录绝对地址
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY='hard to guess string'
    #电子邮件的配置文件
    MAIL_SERVER='smtp.163.com'
    MAIL_PORT=25
    MAIL_USE_TLS=True
    # app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
    # app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX='[确认邮件]'
    FLASKY_MAIL_SENDER='1405065840@qq.com'
    #app.config['FLASKY_ADMIN']=os.environ.get('FLASKY_ADMIN')
    FLASKY_ADMIN=os.environ.get('FLASKY_ADMIN')
    #每页显示的博客数量
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 3
    SSL_DISABLE = False

    @staticmethod
    def init_app(app):
        pass

#开发库，继承Config类
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
#测试库
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
#生产库
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#heroku云平台
class HerokuConfig(DevelopmentConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))
    @classmethod
    def init_app(cls, app):
        DevelopmentConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'heroku': HerokuConfig
}