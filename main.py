# -*- coding:utf-8 -*-
import tkinter as tk
from datetime import datetime

# subject.py のインポート
import subject as sj
import detail_window as dw

# Widgetクラスを別のファイルにしたとき用
# import widget as wg

# ボタンとサブジェクトデータを持つクラス
class Widget(tk.Button):
    def __init__(self):
        self._subject = sj.Subject()
        self._button = tk.Button(bg="#EAECEE", width=14, height=5, borderwidth=0, command=self.button_func)

    # ボタンが押されたときの関数
    def button_func(self):
        app.button_func(self)
        # ボタンが押されたときに全てのボタンを押せなくするためにappの関数を実行している影響で別ファイルにできなかった。
        # 別ファイルにする方法
        # １．ボタンを押せなくしない（Widgetクラスだけで完結させる）
        # ２．ボタンとサブジェクトを別で管理する（そもそも別のクラス必要なくなるが、対応付けが面倒）
        # ３．画期的なアイデア募

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

    # _subjectをそのままを返す
    def get_subject(self):
        return self._subject

    # _subjectの_nameを返す
    def get_sj_name(self):
        return self._subject.get_name()

    # _subjectの課題の中で最も近い締切日を返す
    def get_sj_close_asg_deadline(self):
        return self._subject.get_close_asg_deadline()


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.geometry("800x600")
        self.master.title("TimeTable")
        self._detail_window = None # DetailWindow型の変数
        self._dw_is_opened = False # _detail_windowがすでに開いてるかどうかの変数

        # ラベルを作成、配置
        labelMon = tk.Label(text="月", width = 14, height = 5)
        labelMon.grid(column=1, row=0)
        labelTue = tk.Label(text="火", width = 14, height = 5)
        labelTue.grid(column=2, row=0)
        labelWed = tk.Label(text="水", width = 14, height = 5)
        labelWed.grid(column=3, row=0)
        labelThu = tk.Label(text="木", width = 14, height = 5)
        labelThu.grid(column=4, row=0)
        labelFri = tk.Label(text="金", width=14, height=5)
        labelFri.grid(column=5, row=0)
        labelSat = tk.Label(text="土", fg="#0000F0", width=14, height=5)
        labelSat.grid(column=6, row=0)

        label = tk.Label(text="1", width = 14, height = 5)
        label.grid(column=0, row=1)
        label = tk.Label(text="2", width = 14, height = 5)
        label.grid(column=0, row=2)
        label = tk.Label(text="3", width = 14, height = 5)
        label.grid(column=0, row=3)
        label = tk.Label(text="4", width = 14, height = 5)
        label.grid(column=0, row=4)
        label = tk.Label(text="5", width = 14, height = 5)
        label.grid(column=0, row=5)
        label = tk.Label(text="6", width = 14, height = 5)
        label.grid(column=0, row=6)

        # ウィジェットを作成
        self.widgets = [Widget() for i in range(36)]
        for i in range(6):
            for j in range(6):
                # ウィジェットのボタンを配置
                self.widgets[6*i+j].set_grid(j+1, i+1)

        # テスト用
        self.widgets[6]._subject.set_name("オペレーティングシステム技術")
        self.widgets[6]._subject.add_asg()
        self.widgets[6]._subject.set_asg_name(0, "レポート")
        self.widgets[6]._subject.set_asg_deadline(0, 2022, 2, 20, 23, 55)
        self.widgets[7]._subject.set_name("最適化")
        self.widgets[12]._subject.set_name("ソフトウェア技術")
        self.widgets[12]._subject.add_asg()
        self.widgets[12]._subject.set_asg_name(0, "小テスト")
        self.widgets[12]._subject.set_asg_deadline(0, 2022, 2, 14, 0, 0)
        self.widgets[13]._subject.set_name("数理情報学３")
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


    def button_func(self, widget):
        # ---詳細ウィンドウを開いているときはボタンを押せなくする方法---
        # # detail_windowでの処理が終わるまでボタンを押せなくする
        # for wgt in self.widgets:
        #     wgt.stop_button()
        # # detail_windowを開く関数を実行
        # dw.call_detail_window(widget.get_subject())
        # # detail_windowでの処理が終わったらボタンを押せるようにする
        # for wgt in self.widgets:
        #     wgt.restart_button()
        # ------

        # ---ボタンを押せはするが、ウィンドウは１つしか開かなくする方法---
        if not self._dw_is_opened:
            self._dw_is_opened = True
            self._detail_window = dw.DetailWindow(self, widget.get_subject(), self._dw_is_opened)
            self._detail_window.show_window()
        # ------

    
    # def call_detail_window(self, subject):
        # detail_windowを開く処理（閉じるまで処理を続けるか、閉じたときに何か返してもらえばok）------
        # a = dw.DetailWindow(subject)
        # ---------------------

    
    # 60000ms(1分)ごとにテキストとボタンの色を変更
    def update(self):
        for widget in self.widgets:
            widget.change_text() # テキストの更新
            if widget.get_sj_name() == "":
                widget.set_color("#EAECEE") # 科目名空欄なら初期色
            else:
                if widget.get_sj_close_asg_deadline() == datetime.max:
                    widget.set_color("#D5F5E3") # 課題期限ないなら白
                else:
                    sec = (widget.get_sj_close_asg_deadline() - datetime.now()).total_seconds()
                    if(sec > 604800):
                        widget.set_color("#ABEBC6") # 1週間以上なら緑
                    elif(sec > 259200):
                        widget.set_color("#F8C471") # 3日以上なら黄色
                    else:
                        widget.set_color("#E74C3C") # 3日以内なら赤

        self.after(60000, self.update) # 60000ms後にもう一度実行


##------------------
if __name__ == "__main__":
    app = Application()
    app.update()
    app.mainloop()
