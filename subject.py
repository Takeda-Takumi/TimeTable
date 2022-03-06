# -*- coding:utf-8 -*-
# *** do not edit ***

from datetime import datetime
from copy import copy

class Assignment:
    def __init__(self, name="", deadline=datetime.max):
        self._name = name
        self._deadline = deadline
        self._make_date = datetime.now() #課題の作成時刻

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

    def get_make_date(self): #作成時刻が変化しないようにコピーを返す
        tmp = copy(self._make_date)
        return tmp

    def __str__(self):
        return f"name={self._name} deadline={str(self._deadline)}"

class Subject:
    def __init__(self):
        self._name = ""
        self._assignments = {} #課題名をkeyに取る
        self._memo = ""

    # 課題の数を１つ増やす
    #課題名をキーにとっているため、デフォルト名は＊課題{数字} 最大1万個
    def add_asg(self, assignment = None):
        if assignment == None:
            tname = ""
            cnt = 1
            while( cnt < 10000 ):
                tname=f"*課題{cnt}"
                if not tname in self._assignments:
                    break
                cnt += 1
            assignment = Assignment(name=tname)

        if assignment.get_name() in self._assignments:
            print("課題が重複しています")
            return False
        else:
            self._assignments[assignment.get_name()] = assignment
            return True

    # id番目の課題を削除する（[a, b, c]の中から2番目=bを削除すると[a, c]になる）
    def del_asg(self, id):
        if id < self._asg_num and id >= 0:
            tmp = sorted(self._assignments.values(), key= lambda x: x.get_make_date())
            del self._assignments[tmp[id].get_name()]

    # 科目名を設定する
    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_memo(self, memo):
        self._memo = memo

    def get_memo(self):
        return self._memo

    def get_assigments(self):
        return self._assignments

    # 課題の数を返す
    def get_asg_num(self):
        return len(self._assignments)

    # # id番目の課題の名前を設定する
    def set_asg_name(self, id, name):
        if id < self.get_asg_num() and id >= 0:
            tmp = sorted(self._assignments.values(), key= lambda x: x.get_make_date())
            tmp[id].set_name(name)

    # id番目の課題の締切日を設定する
    def set_asg_deadline(self, id, year, month, day, hour, minutes):
        if id < self.get_asg_num() and id >= 0:
            tmp = sorted(self._assignments.values(), key= lambda x: x.get_make_date())
            tmp[id].set_deadline(year, month, day, hour, minutes)

    # 締切日が最も近い課題の名前を返す
    def get_close_asg_name(self):
        if not self.get_asg_num():
            return ""
        else:
            min_a = min(self._assignments.values(), key = lambda x : x.get_deadline())
        return min_a.get_name()

    # 締切日が最も近い課題の締切日を返す
    def get_close_asg_deadline(self):
        if not self.get_asg_num():
            return datetime.max
        else:
            min_a = min(self._assignments.values(), key = lambda x : x.get_deadline())
        return min_a.get_deadline()
