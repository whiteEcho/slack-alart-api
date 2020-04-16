# coding: utf-8

import json
from flask import Flask
from flask import request
from infrastructure.db_client import HiyariClass
from infrastructure.resource.report import Report

app = Flask(__name__)


@app.route('/hiyari', methods=["GET"])
def index():
    client = HiyariClass()
    return client.list_func()


@app.route('/hiyari', methods=['POST'])
def add():
    form = json.loads(request.get_json())
    report_request: Report = Report(
        form["person"],
        form['date_of_occurred'],
        form['date_of_discovered'],
        form['summary'],
        form['detail']
    )
    client = HiyariClass()
    return client.report_func(report_request)


@app.route('/hiyari/<h_id>', methods=['GET'])
def detail(h_id=None):
    client = HiyariClass()
    return client.detail_func(h_id)


@app.route('/hiyari/<h_id>', methods=['PUT'])
def update(h_id=None):
    form = json.loads(json.loads(request.data))
    report = Report(
        form["person"],
        form['date_of_occurred'],
        form['date_of_discovered'],
        form['summary'],
        form['detail']
    )
    client = HiyariClass()
    return client.update_func(h_id=h_id, report=report)


if __name__ == "__main__":
    app.run()