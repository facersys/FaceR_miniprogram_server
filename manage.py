# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps.Library import db
from apps import create_app

from apps.Moduel.MySQL import notice
from apps.Moduel.MySQL import user

app = create_app()

Migrate(app, db)

# 添加数据库相关命令行
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
