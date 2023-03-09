"""
Created on 2020年2月7日

@author: jianzhihua
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from configs import sysconf

db = SQLAlchemy()
session = db.session
migrate = Migrate(compare_type=True, compare_server_default=True)


def get_database_uri():
    return 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % (
        sysconf.MYSQL_USER, sysconf.MYSQL_PASSWD,
        sysconf.MYSQL_HOST, sysconf.MYSQL_PORT,
        sysconf.MYSQL_DATABASE, sysconf.MYSQL_CHARSET,
    )


def init_db(app: Flask):

    db_uri = get_database_uri()
    app.logger.debug("MYSQL_CONNECT_URL: " + db_uri)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    if sysconf.USE_DB_POOL:
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = sysconf.SQLALCHEMY_ENGINE_OPTIONS

    db.init_app(app)
    migrate.init_app(app, db)
