# -*- coding:utf-8 -*-
import tkinter as tk
from datetime import datetime
import shelve #ファイル保存に関わるライブラリ
import os
from turtle import bgcolor, color # ファイルの存在確認に関わるライブラリ

# 別ファイルのインポート
import detail_window as dw
import widget as wg

BASE_COLOR = "#F9F9F9"
ACCENT_COLOR = "#00ACEE"

class Application(tk.Frame):
    global BASE_COLOR
    global ACCENT_COLOR
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.geometry("800x600")
        self.master.title("TimeTable")
        self._detail_window = dw.DetailWindow(self) # DetailWindow型の変数
        self._dw_is_open = False # _detail_windowがすでに開いてるかどうかの変数

        # ウィジェットを作成
        self.widgets = [wg.Widget() for i in range(36)]
        for i in range(6):
            for j in range(6):
                # ボタンの関数を設定
                self.widgets[6*i+j].set_button_func(self.button_func, self.widgets[6*i+j])
                # ウィジェットのボタンを配置
                self.widgets[6*i+j].set_grid(j+1, i+1)

        if os.path.isfile("timetable.shelve.bak"): # 既に保存したデータがある場合、起動時にデータをロードする
            self.load_timetable()

        self.create_timetable()
        self.input_test_data()


    # ---ボタンを押せはするが、ウィンドウは１つしか開かなくする方法---
    def button_func(self, widget):
        if not self._dw_is_open:
            self._dw_is_open = True
            self._detail_window.set_subject(widget.get_subject())
            self._detail_window.set_func("window_closed", self.dw_close)
            self._detail_window.set_func("on_restore", self.change_text_and_color)
            self._detail_window.show_window()
    
    # ------
    # # ---ボタンを押せなくする方法---
    # def button_func(self, widget):
    #     self.stop_buttons()
    #     self._detail_window = dw.DetailWindow(self, widget.get_subject())
    #     self._detail_window._set_func_restore(self.change_text_and_color)
    #     self._detail_window._set_func(self.dw_close)
    #     has = tk.BooleanVar(value=True)
    #     self._detail_window.show_window(has)
    
    # def stop_buttons(self):
    #     for wgt in self.widgets:
    #         wgt.stop_button()

    # def restart_buttons(self):
    #     for wgt in self.widgets:
    #         wgt.restart_button()
    # # -------


    # widgetsのテキストと色を更新する関数
    def change_text_and_color(self):
        for widget in self.widgets:
            widget.change_text() # テキストの更新
            if widget.get_subj_name() == "" and widget.get_subj_asg_num() == 0:
                widget.set_color("#EAECEE") # 科目名空欄かつ課題数0なら初期色
            else:
                if widget.get_subj_close_asg_deadline() == datetime.max:
                    widget.set_color("#D5F5E3") # 課題期限ないなら白
                else:
                    sec = (widget.get_subj_close_asg_deadline() - datetime.now()).total_seconds()
                    if(sec > 604800):
                        widget.set_color("#ABEBC6") # 1週間以上なら緑
                    elif(sec > 259200):
                        widget.set_color("#F8C471") # 3日以上なら黄色
                    else:
                        widget.set_color("#E74C3C") # 3日以内なら赤

        self.save_timetable()
        self.load_timetable()

    # detail_windowが閉じたときに_dw_is_openとテキスト、色を更新する関数
    def dw_close(self):
        self._dw_is_open = False
        self.change_text_and_color()

    # 60000ms(1分)ごとにテキストとボタンの色を変更
    def update(self):
        self.change_text_and_color()
        self.after(60000, self.update) # 60000ms後にもう一度実行

    # テスト用
    def input_test_data(self):
        self.widgets[6]._subject.set_name("オペレーティングシステム技術")
        self.widgets[6]._subject.add_asg()
        self.widgets[6]._subject.set_asg_name(0, "レポート")
        self.widgets[6]._subject.set_asg_deadline(0, 2022, 2, 20, 23, 55)
        self.widgets[7]._subject.set_name("最適化")
        self.widgets[12]._subject.set_name("ソフトウェア技術")
        self.widgets[12]._subject.add_asg()
        self.widgets[12]._subject.set_asg_name(0, "小テスト")
        self.widgets[12]._subject.set_asg_deadline(0, 2022, 2, 14, 0, 0)
        self.widgets[13]._subject.set_name("数理情報学3")
        self.widgets[15]._subject.set_name("科学技術英語")
        self.widgets[18]._subject.set_name("大規模・高速計算")
        self.widgets[18]._subject.add_asg()
        self.widgets[18]._subject.set_asg_name(0, "レポート")
        self.widgets[18]._subject.set_asg_deadline(0, 2022, 2, 14, 23, 55)
        self.widgets[19]._subject.set_name("開発系プログラミング演習")
        self.widgets[19]._subject.add_asg()
        self.widgets[19]._subject.set_asg_name(0, "週課題")
        self.widgets[19]._subject.set_asg_deadline(0, 2022, 2, 15, 15, 0)
        self.widgets[20]._subject.set_name("マルチメディア情報処理")
        self.widgets[20]._subject.add_asg()
        self.widgets[20]._subject.set_asg_name(0, "週課題")
        self.widgets[20]._subject.set_asg_deadline(0, 2022, 2, 16, 15, 0)

    # ラベルを作成、配置
    def create_timetable(self):
        labelMon = tk.Label(text="月", width = 14, height = 5, bg = BASE_COLOR)
        labelMon.grid(column=1, row=0)
        labelTue = tk.Label(text="火", width = 14, height = 5, bg = BASE_COLOR)
        labelTue.grid(column=2, row=0)
        labelWed = tk.Label(text="水", width = 14, height = 5, bg = BASE_COLOR)
        labelWed.grid(column=3, row=0)
        labelThu = tk.Label(text="木", width = 14, height = 5, bg = BASE_COLOR)
        labelThu.grid(column=4, row=0)
        labelFri = tk.Label(text="金", width=14, height=5, bg = BASE_COLOR)
        labelFri.grid(column=5, row=0)
        labelSat = tk.Label(text="土", fg="#0000F0", width=14, height=5, bg = BASE_COLOR)
        labelSat.grid(column=6, row=0)

        label = tk.Label(text="1", width = 14, height = 5, bg = BASE_COLOR)
        label.grid(column=0, row=1)
        label = tk.Label(text="2", width = 14, height = 5, bg = BASE_COLOR)
        label.grid(column=0, row=2)
        label = tk.Label(text="3", width = 14, height = 5, bg = BASE_COLOR)
        label.grid(column=0, row=3)
        label = tk.Label(text="4", width = 14, height = 5, bg = BASE_COLOR)
        label.grid(column=0, row=4)
        label = tk.Label(text="5", width = 14, height = 5, bg = BASE_COLOR)
        label.grid(column=0, row=5)
        label = tk.Label(text="6", width = 14, height = 5, bg = BASE_COLOR)
        label.grid(column=0, row=6)

    def save_timetable(self):
        with shelve.open("timetable.shelve",) as file:
            for i in range(len(self.widgets)):
                file[str(i)] = self.widgets[i].get_subject()

    def load_timetable(self):
        with shelve.open("timetable.shelve",) as file:
            for i in range(len(self.widgets)):
                self.widgets[i].set_subject(file[str(i)])




##------------------
if __name__ == "__main__":
    app = Application()
    app.update()
    app.mainloop()
