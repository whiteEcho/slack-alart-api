# coding: utf-8


class Report:
    person = None
    date_of_occurred = None
    date_of_discovered = None
    summary = None
    detail = None

    def __init__(self, person, date_of_occurred, date_of_discovered, summary, detail):
        self.person = person
        self.date_of_occurred = date_of_occurred
        self.date_of_discovered = date_of_discovered
        self.summary = summary
        self.detail = detail
