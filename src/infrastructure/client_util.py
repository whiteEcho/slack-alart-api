# encode:utf-8

from datetime import datetime

import cx_Oracle as co

from . import db_config as conf


def create_connect():
    tns = co.makedsn(conf.HOST, conf.PORT, conf.SERVICE)
    connect = co.connect(user=conf.DB_USER, password=conf.DB_PASS, dsn=tns, encoding='utf-8')

    return connect


def time_formatter(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%Y/%m/%d")
