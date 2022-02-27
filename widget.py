# -*- coding:utf-8 -*-
import tkinter as tk
from functools import partial

# subject.py のインポート
import subject as subj

BASE_COLOR = "#F9F9F9"
ACCENT_COLOR = "#00ACEE"
class Widget(tk.Button):
    global BASE_COLOR
    global ACCENT_COLOR
    
    def __init__(self, w, h):
        self._func = lambda self:print("ボタンを押したときの関数をセットしてください")
        self._subject = subj.Subject()
        self._button = tk.Button(bg=BASE_COLOR, width = w, height=h, borderwidth=0, command=self.button_func)
        # self._button.place(width=w, height=h)

    # ボタンが押されたときに実行する関数をセットする関数。
    # Widget.set_button_func(<ボタンを押したときに実行する関数>, 引数1, 引数2, …)でセット可能。
    def set_button_func(self, func, *args):
        self._func = partial(func, *args)

    # ボタンが押されたときの関数
    def button_func(self):
        self._func() # セットした関数を実行する。

    # ボタンを配置する
    def set_grid(self, c, r):
        self._button.grid(column=c, row=r)

    # 表示するテキストを変更する
    def change_text(self):
        if self._subject.get_asg_num() == 0: # 課題の数が0なら科目名のみ
            self._button["text"] = self._subject.get_name()
        else: # 科目名\n締切が最も近い課題名\n最も近い締切日
            self._button["text"] = self._subject.get_name()+"\n"+self._subject.get_close_asg_name()+"\n"+self._subject.get_close_asg_deadline().strftime("%Y/%m/%d/%H:%M")

    # ボタンの色を変える
    def set_color(self, color):
        self._button["bg"] = color

    # ボタンを押せなくする
    def stop_button(self):
        self._button["state"] = tk.DISABLED

    # ボタンを押せるようにする
    def restart_button(self):
        self._button["state"] = tk.NORMAL

    # _subjectを設定する
    def set_subject(self, new_subject):
        if(type(new_subject) == subj.Subject):
            self._subject = new_subject
        else:
            print("set_subject()の引数がSubject型ではありません")

    # _subjectをそのままを返す
    def get_subject(self):
        return self._subject

    # _subjectの_nameを返す
    def get_subj_name(self):
        return self._subject.get_name()

    # _subjectの_asg_numを返す
    def get_subj_asg_num(self):
        return self._subject.get_asg_num()

    # _subjectの課題の中で最も近い締切日を返す
    def get_subj_close_asg_deadline(self):
        return self._subject.get_close_asg_deadline()

if __name__ == "__main__":
    pass
