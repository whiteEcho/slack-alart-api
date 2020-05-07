# coding: utf-8

from werkzeug.exceptions import BadRequest


class Report:
    reporter = None
    date_of_occurred = None
    date_of_discovered = None
    summary = None
    detail = None

    def __init__(self, reporter, date_of_occurred, date_of_discovered, summary, detail):
        if reporter and date_of_discovered and summary:
            self.reporter = reporter
            self.date_of_occurred = date_of_occurred
            self.date_of_discovered = date_of_discovered
            self.summary = summary
            self.detail = detail
        else:
            raise BadRequest
