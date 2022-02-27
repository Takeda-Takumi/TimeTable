import tkinter as tk
from tkinter import ttk
from datetime import date, datetime
import subject as sb
import custom_widgets as cw

from functools import partial

_base_color='#F9F9F9'
_accent_color='#00ACEE'

# 課題入力用クラス
class InputAssignment:
    def __init__(self, master=None):
        self._master=master
        self._asig=sb.Assignment()
        self._funcs={}

        tmp = ["on_ok_button"]
        for i in tmp:
            self._funcs[i]= ( lambda : { } )

    def get(self):
        return self._asig

    def set_func(self, sequence, func, *args):
        if sequence in self._funcs:
            self._funcs[sequence] = partial(func, *args)

    def make_window(self):

        default_name = "最適化レポート"
        # default_deadline = "2022/12/08/12/34"

        ass_win = tk.Toplevel(self._master)
        ass_win.geometry("670x120")
        ass_win.title("課題追加")
        ass_win.option_add("*Font","bold 20")
        # ass_win.lift()
        ass_win.attributes("-topmost",True)

        # 課題名用フレーム
        frame_name=tk.Frame(ass_win)
        frame_name.pack(side="top",fill='both', expand=True)
        frame_name.config(bg=_base_color)

        # 課題名ラベル
        label_name = tk.Label(frame_name)
        label_name.config(text = "課題名:",bg=_base_color)
        label_name.pack(side='left')

        # 課題名入力
        ent_name = tk.Entry(frame_name,fg="gray")
        ent_name.insert(0,default_name)

        def clear(event):
            ent_name["fg"]="black"
            if ent_name.get() == default_name:
                ent_name.delete(0,len(ent_name.get()))

        ent_name.bind("<Button-1>",clear)
        ent_name.pack(side="left")

        # 期限用フレーム
        frame_deadline=tk.Frame(ass_win)
        frame_deadline.pack(side="top",fill='both', expand=True)
        frame_deadline.config(bg=_base_color)

        # 期限ラベル
        label_deadline = tk.Label(frame_deadline)
        label_deadline.config(text = "提出期限:",bg=_base_color)
        label_deadline.pack(side="left")

        today=date.today()
        # print(today.year)
        # print(type(today.year))
        default_year_index=today.year-2022
        default_month_index=today.month-1
        default_day_index=today.day-1

        # 期限入力用combobox
        year_values=[i for i in range(2022, 3000)]
        month_values=[i for i in range(1, 13)]
        day_values=[i for i in range(1, 32)]
        hour_values=[i for i in range(0, 24)]
        minute_values=[i for i in range(1, 60)]

        year_combobox = ttk.Combobox(frame_deadline,width=4,values=year_values)
        year_combobox.current(default_year_index)
        year_combobox.pack(side="left")
        year_combobox.pack()

        label_year = tk.Label(frame_deadline)
        label_year.config(text = "年",bg=_base_color)
        label_year.pack(side="left")
        label_year.pack()

        month_combobox = ttk.Combobox(frame_deadline,width=2,values=month_values)
        month_combobox.current(default_month_index)
        month_combobox.pack(side="left")
        month_combobox.pack()

        label_month = tk.Label(frame_deadline)
        label_month.config(text = "月",bg=_base_color)
        label_month.pack(side="left")
        label_month.pack()

        day_combobox = ttk.Combobox(frame_deadline,width=2,values=day_values)
        day_combobox.current(default_day_index)
        day_combobox.pack(side="left")
        day_combobox.pack()

        label_day = tk.Label(frame_deadline)
        label_day.config(text = "日",bg=_base_color)
        label_day.pack(side="left")
        label_day.pack()

        hour_combobox = ttk.Combobox(frame_deadline,width=2,values=hour_values)
        hour_combobox.current(len(hour_values)-1)
        hour_combobox.pack(side="left")
        hour_combobox.pack()

        label_hour = tk.Label(frame_deadline)
        label_hour.config(text = "時",bg=_base_color)
        label_hour.pack(side="left")
        label_hour.pack()

        minute_combobox = ttk.Combobox(frame_deadline,width=2,values=minute_values)
        minute_combobox.current(len(minute_values)-1)
        minute_combobox.pack(side="left")
        minute_combobox.pack()

        label_minute = tk.Label(frame_deadline)
        label_minute.config(text = "分",bg=_base_color)
        label_minute.pack(side="left")
        label_minute.pack()

        def mouse_on(e):
            ok_button['fg'] = _accent_color
        def mouse_leave(e):
            # ok_button['background'] = '#E6E3E2'
            ok_button['fg'] = 'gray'

        def buttonclicked():
            _name = ent_name.get()
            # assignment.set_name(_name)
            self._asig.set_name(_name)
            year = int(year_combobox.get())
            month = int(month_combobox.get())
            day = int(day_combobox.get())
            hour = int(hour_combobox.get())
            minute = int(minute_combobox.get())

            self._asig.set_deadline(year, month, day, hour, minute)
            self._funcs["on_ok_button"]()
            ass_win.destroy()

        # 完了ボタン
        ok_button = tk.Button(frame_deadline,bg=_base_color,text = "Add",fg='gray',relief="flat",overrelief="flat",command=buttonclicked)
        # ok_button = tk.Button(frame_deadline,text = "Add",fg='gray',relief="flat",overrelief="flat",command=buttonclicked)
        # ok_button = tk.Button(frame_deadline,text = "OK",relief="groove",overrelief="raised",command=buttonclicked)
        ok_button.pack(side="left")
        ok_button.bind("<Enter>", mouse_on)
        ok_button.bind("<Leave>", mouse_leave)

    #     assignment = sb.Assignment()
    # assignment.set_name("数値計算_第２回レポート")
    # assignment.set_deadline(2022,8,8,12,34)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x300")

    ina = InputAssignment(root)
    bt1 = tk.Button(text="input assignment", command=ina.make_window)
    bt1.pack()
    ina.set_func( "on_ok_button", lambda: print("on_ok") )


    bt2 = tk.Button(text="print assignment", command = lambda : print(ina.get()))
    bt2.pack()

    root.mainloop()
