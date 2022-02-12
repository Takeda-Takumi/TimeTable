# -*- coding:utf-8 -*-
# *** do not edit ***

from datetime import datetime

class Assignment:
    def __init__(self):
        self._name = ""
        self._deadline = datetime.max

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_deadline(self, year, month, day, hour, minutes):
        self.deadline = datetime(year, month, day, hour, minutes)

    def get_deadline(self):
        return self._deadline


class Subject:
    def __init__(self):
        self._name = ""
        self._assignments = [Assignment() for i in range(1)]
        self._memo = ""

    def add_asg(self):
        self._assignments.append()

    def del_asg(self):
        # dareka kaitoite kudasai
        return

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name
    
    def set_memo(self, memo):
        self._memo = memo

    def get_memo(self):
        return self._memo


class Timetable:
    def __init__(self):
        self._subjects = [Subject() for i in range(36)]
