# -*- coding:utf-8 -*-
# *** do not edit ***

from datetime import datetime

class Assignment:
    def __init__(self):
        self._name = ""
        self._deadline = datetime.max

    # 課題名を設定する
    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    # 分単位まで設定する
    def set_deadline(self, year, month, day, hour, minutes):
        self._deadline = datetime(year, month, day, hour, minutes)

    def get_deadline(self):
        return self._deadline


class Subject:
    def __init__(self):
        self._name = ""
        self._assignments = []
        self._memo = ""
        self._asg_num = 0

    # 課題の数を１つ増やす
    def add_asg(self):
        self._assignments.append(Assignment())
        self._asg_num += 1

    # id番目の課題を削除する（[a, b, c]の中から2番目=bを削除すると[a, c]になる）
    def del_asg(self, id):
        if id < self._asg_num and id >= 0:
            del self._assignments[id]
            self._asg_num -= 1

    # 科目名を設定する
    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name
    
    def set_memo(self, memo):
        self._memo = memo

    def get_memo(self):
        return self._memo

    # 課題の数を返す
    def get_asg_num(self):
        return self._asg_num

    # id番目の課題の名前を設定する
    def set_asg_name(self, id, name):
        if id < self._asg_num and id >= 0:
            self._assignments[id].set_name(name)

    # id番目の課題の締切日を設定する
    def set_asg_deadline(self, id, year, month, day, hour, minutes):
        if id < self._asg_num and id >= 0:
            self._assignments[id].set_deadline(year, month, day, hour, minutes)

    # 締切日が最も近い課題の名前を返す
    def get_close_asg_name(self):
        if self._asg_num == 0:
            return ""
        else:
            min_d = self._assignments[0].get_deadline()
            min_n = self._assignments[0].get_name()
            for i in range(1, self._asg_num):
                if min_d > self._assignments[i].get_deadline():
                    min_d = self._assignments[i].get_deadline()
                    min_n = self._assignments[i].get_name()

            return min_n

    # 締切日が最も近い課題の締切日を返す
    def get_close_asg_deadline(self):
        if self._asg_num == 0:
            return datetime.max
        else:
            min_d = self._assignments[0].get_deadline()
            for i in range(1, self._asg_num):
                if min_d > self._assignments[i].get_deadline():
                    min_d = self._assignments[i].get_deadline()

            return min_d
