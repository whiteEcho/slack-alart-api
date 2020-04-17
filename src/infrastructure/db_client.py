# coding: utf-8

from datetime import datetime
import json
import os

import cx_Oracle as co

from .resource.report import Report
from . import db_config as conf

os.environ['NLS_LANG'] = 'JAPANESE_JAPAN.AL32UTF8'


class HClient:

    def list_func(self):
        connect = self.__create_connect()
        cursor = connect.cursor()
        cursor.execute('select id,summary from h_info order by id')

        rows = cursor.fetchall()

        response = []
        for row in rows:
            dic = {
                'id': row[0],
                'summary': row[1]
            }

            response.append(dic)

        return json.dumps({'response': response})

    def detail_func(self, h_id):
        connect = self.__create_connect()
        cursor = connect.cursor()
        cursor.execute('select * from h_info where id=:id', id=h_id)

        rows = cursor.fetchall()
        row = {
            'id': rows[0][0],
            'reporter': rows[0][1],
            'date_of_occurred': rows[0][2] if rows[0][2] else '---',
            'date_of_discovered': rows[0][3],
            'summary': rows[0][4],
            'detail': rows[0][5] if rows[0][5] else '---'
        }

        return json.dumps(row, default=self.__time_formatter)

    def report_func(self, report: Report):
        connect = self.__create_connect()
        cursor = connect.cursor()
        sql = '''insert 
        into h_info(reporter, date_of_occurred, date_of_discovered, summary, detail, created_at, updated_at) 
        values(:reporter, :occurred, :discovered, :summary, :detail, systimestamp, systimestamp)'''
        cursor.execute(sql,
                       reporter=report.reporter,
                       occurred=report.date_of_occurred,
                       discovered=report.date_of_discovered,
                       summary=report.summary,
                       detail=report.detail
                       )
        connect.commit()

        return self.__insert_select()

    def update_func(self, h_id, report: Report):
        connect = self.__create_connect()
        cursor = connect.cursor()
        sql = '''update h_info
        set
        reporter=:reporter,
        date_of_occurred=:occurred,
        date_of_discovered=:discovered,
        summary=:summary,
        detail=:detail,
        updated_at=systimestamp
        where
        id=:id'''
        cursor.execute(sql,
                       reporter=report.reporter,
                       occurred=report.date_of_occurred,
                       discovered=report.date_of_discovered,
                       summary=report.summary,
                       detail=report.detail,
                       id=h_id)
        connect.commit()
        return self.detail_func(h_id)

    def __insert_select(self):
        connect = self.__create_connect()
        cursor = connect.cursor()
        cursor.execute(
            'select id,reporter,summary from h_info where id=(select max(id) from h_info)')

        rows = cursor.fetchall()
        row = {
            'id': rows[0][0],
            'reporter': rows[0][1],
            'summary': rows[0][2]
        }
        return json.dumps(row)

    @staticmethod
    def __create_connect():
        tns = co.makedsn(conf.HOST, conf.PORT, conf.SERVICE)
        connect = co.connect(user=conf.DB_USER, password=conf.DB_PASS, dsn=tns, encoding='utf-8')

        return connect

    @staticmethod
    def __time_formatter(obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y/%m/%d")
