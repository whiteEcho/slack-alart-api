# coding: utf-8

import codecs
import json
import os

from . import client_util as util
from .resource.report import Report

os.environ['NLS_LANG'] = 'JAPANESE_JAPAN.AL32UTF8'


class HClient:

    @staticmethod
    def list_func():
        connect = util.create_connect()
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

    @staticmethod
    def detail_func(h_id):
        connect = util.create_connect()
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

        return json.dumps(row, default=util.time_formatter)

    def report_func(self, report: Report):
        connect = util.create_connect()
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
        connect = util.create_connect()
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

    @staticmethod
    def __insert_select():
        connect = util.create_connect()
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


class IClient:

    @staticmethod
    def list_func():
        connect = util.create_connect()
        cursor = connect.cursor()
        cursor.execute('select id,category,summary,create_at from i_info')
        rows = cursor.fetchall()

        results = []
        for row in rows:
            result = {
                'id': row[0],
                'category': row[1],
                'summary': row[2],
                'report_date': row[3]
            }

            results.append(result)

        return json.dumps({'response': results}, default=util.time_formatter)

    @staticmethod
    def detail_func(i_id):
        connect = util.create_connect()
        cursor = connect.cursor()
        cursor.execute('select org_file_name, report from i_info where id=:id', id=i_id)
        row = cursor.fetchall()[0]
        return row[0], row[1].read()

    def report_func(self, category, summary, file_name, file_path):
        connect = util.create_connect()
        cursor = connect.cursor()
        sql = '''insert
        into i_info(category, summary, report, org_file_name ,create_at, update_at)
        values(:category, :summary, :data, :file_name, systimestamp, systimestamp)'''

        with codecs.open(file_path, mode='r+b') as f:
            cursor.execute(sql,
                           category=category,
                           summary=summary,
                           file_name=file_name,
                           data=f.read())
            connect.commit()

        return {'id': self.__insert_select()}

    @staticmethod
    def update_func(i_id, category, summary, file_name, file_path):
        connect = util.create_connect()
        cursor = connect.cursor()
        sql = '''update i_info
        set
        category=:category,
        summary=:summary,
        org_file_name=:file_name,
        report=:report,
        update_at=systimestamp
        where
        id=:i_id'''

        with codecs.open(file_path, mode='r+b') as f:
            cursor.execute(sql,
                           category=category,
                           summary=summary,
                           file_name=file_name,
                           report=f.read(),
                           i_id=i_id)
            connect.commit()

    @staticmethod
    def __insert_select():
        connect = util.create_connect()
        cursor = connect.cursor()
        cursor.execute('select max(id) from i_info')
        return cursor.fetchall()[0][0]
