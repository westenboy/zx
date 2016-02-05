#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
from app import create_app, db
from app.models import User, Role,Permission,Post,Follow
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)
'''MigrateCommand类的命令通过db添加到shell中
   python zhuxiang.py db init 创建migrations文件夹，即创建迁移仓库
   python zhuxiang.py db migrate -m "generate upgrade() 函数" 根据模型生成upgrade函数
   python zhuxiang.py db upgrade 根据模型运行upgrade()函数里的建表语句
'''
manager.add_command('db',MigrateCommand)

#增加这个函数，python zhuxiang.py shell时就不用再from zhuxiang import xxx
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Permission=Permission,Post=Post,Follow=Follow)
manager.add_command("shell",Shell(make_context=make_shell_context))

#增加test命令，这样通过python zhuxiang.py test就可以启动单元测试类
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
if __name__ == '__main__':
    app.run()
