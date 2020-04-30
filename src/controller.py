# coding: utf-8

import codecs
import hashlib
import json
import os

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError
from flask import Flask
from flask import request
from flask import make_response

from service.incident_service import IncidentService
from infrastructure.db_client import HClient
from infrastructure.db_client import IClient
from infrastructure.resource.report import Report

app = Flask(__name__)


@app.route('/hiyari', methods=["GET"])
def index():
    client = HClient()
    return client.list_func()


@app.route('/hiyari', methods=['POST'])
def add():
    form = json.loads(request.get_json())
    report_request: Report = Report(
        form["reporter"],
        form['date_of_occurred'],
        form['date_of_discovered'],
        form['summary'],
        form['detail']
    )
    client = HClient()
    return client.report_func(report_request)


@app.route('/hiyari/<h_id>', methods=['GET'])
def detail(h_id=None):
    client = HClient()
    return client.detail_func(h_id)


@app.route('/hiyari/<h_id>', methods=['PUT'])
def update(h_id=None):
    form = json.loads(json.loads(request.file_name))
    report = Report(
        form["reporter"],
        form['date_of_occurred'],
        form['date_of_discovered'],
        form['summary'],
        form['detail']
    )
    client = HClient()
    return client.update_func(h_id=h_id, report=report)


@app.route('/incident', methods=['GET'])
def incident_list():
    client = IClient()
    return client.list_func()


@app.route('/incident', methods=['POST'])
def incident_add():
    file_name = request.headers['file_name']
    data = request.data
    file_path = os.path.join('temp', '{}.xlsx'.format(hashlib.sha256(data).hexdigest()))

    try:
        with codecs.open(file_path, mode='x+b') as f:
            f.write(data)
        service = IncidentService(file_name, file_path)
        result = service.add()
    finally:
        if os.path.isfile(file_path):
            os.remove(file_path)

    return result


@app.route('/incident/<i_id>', methods=['GET'])
def incident_detail(i_id=None):
    client = IClient()
    file_name, data = client.detail_func(i_id)
    response = make_response()
    response.mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['file_name'] = file_name
    response.data = data
    return response


@app.route('/incident/<i_id>', methods=['PUT'])
def incident_update(i_id=None):
    file_name = request.headers['file_name']
    data = request.data
    file_path = os.path.join('temp', '{}.xlsx'.format(hashlib.sha256(data).hexdigest()))

    try:
        with codecs.open(file_path, mode='x+b') as f:
            f.write(data)
        service = IncidentService(file_name, file_path)
        service.update(i_id)

        return make_response('', 200)
    finally:
        if os.path.isfile(file_path):
            os.remove(file_path)


@app.errorhandler(NotFound)
def error_404(e):
    error = {
        'code': '001',
        'message': 'not found'
    }
    return error, 404


@app.errorhandler(BadRequest)
def error_400(e):
    error = {
        'code': '002',
        'message': 'bad request!'
    }
    return error, 400


@app.errorhandler(InternalServerError)
def error_500(e):
    error = {
        'code': '999',
        'message': 'internal server error'
    }
    return error, 500


if __name__ == "__main__":
    app.run()
