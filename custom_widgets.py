import tkinter as tk
import re

#keys, configure関数必須
class RestoreConfigure:
    """
    class RestoreConfigure
        widgetの設定値を保存するクラス
        また、保存した設定をwidgetに反映することも可能
        (*) .configure関数と.cget関数必須

    -----------------
    関数リファレンス
    get         : 設定値を保持する辞書を得る
    configure   : 設定値を変更する
    """

    def __init__(self, widget):
        """
        初期化関数

        Parameters
        -----------------
        widget : tk.Widget
            設定値保存する対象のウィジェット(.configure関数と.cget関数必須)
        """
        self._con={}
        self._alias={}

        for key, value in widget.configure().items():
            if type(value) == type(()):
                for i in value:
                    if type(i) == type(""):
                        tmp = list(i)
                        if  len(tmp) > 0 and tmp[0] == '-':
                            self._alias[key]=i[1:]
                            self._alias[i[1:]]=key

        for key in widget.keys():
            self._con[key] = widget.cget(key)

    def get(self):
        """
        設定値を保持する辞書を得る

        Returns
        -----------------
        con : dict
            設定名をキー、設定値を値にもつ辞書

        Notes
        -----------------
        コンストラクタに使用したウィジェットと同じ型のウィジェットにこの辞書を設定することで、
        保存している設定を反映させることができる。
            ex) w  : tk.Widget
                rc : RestoreConfigure
                w.configure( rc.get() )
        """
        return self._con

    def configure(self, **kwargs):
        """
        設定値を変更する

        Parameters
        -----------------
            sequence = value ( 通常のconfigure関数と同様)
        """
        for key, value in kwargs.items():
            self._set(key, value)

    def _set(self, key, value):
        if not key in self._con:
            print("[Error] Not proper key")
            return
        if key in self._alias:
            self._con[self._alias[key]] = value
        self._con[key] = value

    def __getitem__(self, key):
        return self._con[key]

    def __setitem__(self, key, value):
        self._set(key,value)

    def __len__(self):
        return len(self._con)

class GuideEntry(tk.Entry):
    """
    GideEntry
        Guide付き Entryを生成するクラス
        (未入力の際にガイドテキストを表示する)

    ----------------
    関数リファレンス

    get             : Entry内のテキストを取得する
    insert          : Entryにテキストを挿入する
    set_alpha_str   : ガイドテキストを設定する
    set_alpha_color : ガイドテキストの色を設定する
    ----以下の関数はEntryのメンバ関数と同様---------
    configure
    bind
    pack
    """

    def __init__(self, master=None, **kwargs):
        """
        初期化関数

        Notes
        -------------
        オプションなどはEntryの初期化と同様
        """
        super().__init__(master)
        self._alpha_str = ""
        self._alpha_color= "SystemWindowText"
        self._entry = tk.Entry(master, kwargs)
        self._strv = tk.StringVar(value= "")
        self._entry.configure(textvariable = self._strv)

    def get(self):
        """
        Entry内のテキストを取得する

        Returns
        -------------
        text : String
            Entry内のテキスト
        """
        if ( self._strv.get() == self._alpha_str):
            return ""
        return self._strv.get()

    def insert(self, str):
        """
        Entry内にテキストを挿入する

        Parameters
        -------------
        str : String
            Entry内に挿入するテキスト
        """
        self._strv.set(str)

    def set_alpha_str(self, str):
        """
        ガイドテキストの文字列を設定する

        Parameters
        -------------
        str : String
            ガイドテキストに設定する文字列
        """
        self._alpha_str=str

    def set_alpha_color(self, color ):
        """
        ガイドテキストの色を設定する

        Parameters
        -------------
        color : String
            ガイドテキストに設定する色(指定形式はTkinterと同様)
        """
        self._alpha_color=color

    def configure(self, **kwargs):
        self._entry.configure(kwargs)

    def bind(self, *args):
        self._entry.bind(*args)

    def pack(self, **kwargs):
        self._fg_color=self._entry.cget("fg")
        self._entry.pack(kwargs)

        def _mode_init(e):
            self._entry.icursor(0)
            self._entry.bind("<KeyPress>", _mode_wait)

        def _mode_wait(e):
            self._strv.set("")
            self._entry.configure(fg=self._fg_color)
            self._entry.unbind("<KeyPress>")
            self._entry.unbind("<ButtonRelease>")
            self._entry.bind("<KeyRelease>", _mode_enter)


        def _mode_enter(e):
            if self._strv.get() == "":
                self._entry.configure(fg=self._alpha_color)
                self._strv.set(self._alpha_str)
                self._entry.icursor(0)
                self._entry.bind("<KeyPress>", _mode_wait)
                self._entry.bind("<ButtonRelease>", _mode_init)

        if ( self._strv.get() == "" ):
            self._entry.config(fg=self._alpha_color)
            self._strv.set(self._alpha_str)
            self._entry.bind("<ButtonRelease>", _mode_init)
        else:
            self._entry.bind("<KeyRelease>", _mode_enter)


#スクロールすることができるフレーム
class ScrollFrame(tk.Frame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master)
        self._outframe=tk.Frame(master)
        self._canvas = tk.Canvas(self._outframe,bg="khaki2")
        self._inframe = tk.Frame(self._canvas, kwargs, pady = 10, bg="khaki2")
        self._scrollbar_y = tk.Scrollbar(self._outframe, orient=tk.VERTICAL, command=self._canvas.yview)

        self._inframe.bind("<Configure>", self._adjust)
        self._outframe.bind("<Map>", self._adjust)
        self._inframe.bind("<MouseWheel>", self._mouse_y_scroll)
        self._canvas.create_window(0,0,window = self._inframe, anchor="c", )
        self._canvas.config(yscrollcommand=self._scrollbar_y.set)

        self._canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self._scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    def _adjust(self, e):
        maxw, maxh = 0, 0
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        for w in self._inframe.winfo_children():
            maxw = max(maxw, w.winfo_width())
        if ( maxw == 0 ):
            maxw = 200
        self._canvas.configure(width=maxw)

    def _mouse_y_scroll(self, event):
        if event.delta > 0:
            self._canvas.yview_scroll(-1, 'units')
        elif event.delta < 0:
            self._canvas.yview_scroll(1, 'units')

    #canvasの設定変更
    def canvas_config(self, **kwargs):
        self._canvas.configure(kwargs)

    #outframeの設定変更
    def outframe_config(self, **kwargs):
        self._outframe.configure(kwargs)

    #含めるwidgetの親となるframeを返す
    def get(self):
        return self._inframe

    def pack(self, **kwargs):
        self._outframe.pack(kwargs)

    def grid(self, **kwargs):
        self._outframe.grid(kwargs)

    def pack_widget(self, widget, **kwargs):
        widget.bind("<MouseWheel>", self._mouse_y_scroll)
        widget.pack(kwargs)

class GuideButton(tk.Button):
    """
    カーソルによるガイドを行うボタンウィジェット
    ------------

    関数リファレンス
    set_switch      : ガイド機能のON/OFFの切り替え
    config_default  : 非ガイド時のボタンを設定する
    config_selected : ガイド時のボタンを設定する
    ----以下の関数はEntryのメンバ関数と同様---------
    pack
    bind

    Notes
    ------------
    注意点:初期化以外の場合、commandが反映されるのにラグが生じる
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master)
        self._bt = tk.Button(master, kwargs)
        self._dconfig=RestoreConfigure(self._bt)
        self._sconfig=RestoreConfigure(self._bt)
        self._change=True
        self._selected=False

    def set_switch(self, bool):
        """
        ガイド機能のON/OFFを切り替える

        Parameters
        ------------
        bool : boolean
            ガイド機能の有無を表す
                True : ON    False: OFF
        """

        self._change=bool
        if ( self._change and self._selected ):
            self._bt.configure(self._sconfig.get())

    def config_default(self, **kwargs):
        """
        非ガイド時のボタンを設定する

        Parameters
        ------------
        sequence = value ( 通常のconfigure関数と同様)
        """
        self._dconfig.configure(**kwargs)
        if (not self._selected) and self._change:
            self._bt.configure(self._dconfig.get())

    def config_selected(self, **kwargs):
        """
        ガイド時のボタンを設定する

        Parameters
        ------------
        sequence = value ( 通常のconfigure関数と同様)
        """
        self._sconfig.configure(**kwargs)
        if self._selected and self._change:
            self._bt.configure(self._sconfig.get())

    def pack(self, **kwargs):
        self._bt.bind("<Enter>", self._active)
        self._bt.bind("<Leave>", self._inactive)

        self._bt.configure(self._dconfig.get())
        self._bt.pack(kwargs)

    def bind(self, **kwargs):
        self._bt.bind(kwargs)

    def _active(self,e):
        if self._change:
            self._bt.configure(self._sconfig.get())
        self._rev()

    def _inactive(self,e):
        if self._change:
            self._bt.configure(self._dconfig.get())
        self._rev()

    def _rev(self):
        self._selected= ( not self._selected)

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Main Window")
    root.geometry("300x200")

    def func():
        print("gb_selected=", gb._selected)
        gb.set_switch(True)

    gb = GuideButton(root, text="Guide Button", command=func)
    gb.config_selected(bg="Khaki2")
    gb.config_default(bg="Medium purple1", fg="ghostwhite")
    gb.set_switch(False)
    gb.pack(side=tk.LEFT)


    gb.config_selected(command=func)
    root.mainloop()
