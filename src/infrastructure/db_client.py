# coding: utf-8

import cx_Oracle as co
import json
import os
from datetime import datetime
from .resource.report import Report

os.environ['NLS_LANG'] = 'JAPANESE_JAPAN.AL32UTF8'


class HiyariClass:
    host = '127.0.0.1'
    port = 1521
    service = "orcl"
    user = "dev"
    password = "dev"

    def __init__(self):
        pass

    def list_func(self):
        connect = self.__create_connect()
        cursor = connect.cursor()
        cursor.execute('select id,summary from basic_info order by id')

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
        cursor.execute('select * from basic_info where id=:id', id=h_id)

        rows = cursor.fetchall()
        row = {
            'id': rows[0][0],
            'person': rows[0][1],
            'date_of_occurred': rows[0][2],
            'date_of_discovered': rows[0][3],
            'summary': rows[0][4],
            'detail': rows[0][5]
        }

        return json.dumps(row, default=self.__time_formatter)

    def report_func(self, report: Report):
        connect = self.__create_connect()
        cursor = connect.cursor()
        sql = '''insert 
        into basic_info(person, date_of_occured, date_of_discoverd, summary, detail) 
        values(:person, :occured, :discovred, :summary, :detail)'''
        cursor.execute(sql,
                       person=report.person,
                       occured=report.date_of_occurred,
                       discovred=report.date_of_discovered,
                       summary=report.summary,
                       detail=report.detail
                       )
        connect.commit()

        return self.__insert_select()

    def update_func(self, h_id, report: Report):
        connect = self.__create_connect()
        cursor = connect.cursor()
        sql = '''update basic_info
        set
        person=:person,
        date_of_occured=:occurred,
        date_of_discoverd=:discovered,
        summary=:summary,
        detail=:detail
        where
        id=:id'''
        cursor.execute(sql,
                       person=report.person,
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
            'select id,person,summary from basic_info where id=(select max(id) from basic_info)')

        rows = cursor.fetchall()
        row = {
            'id': rows[0][0],
            'person': rows[0][1],
            'summary': rows[0][2]
        }
        return json.dumps(row)

    @classmethod
    def __create_connect(cls):
        tns = co.makedsn(cls.host, cls.port, cls.service)
        connect = co.connect(user=cls.user, password=cls.password, dsn=tns, encoding='utf-8')

        return connect

    @staticmethod
    def __time_formatter(obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y/%m/%d")
