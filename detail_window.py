import tkinter as tk
import tkinter.font as f

import subject as sb
import custom_widgets as cw
import input_assignment as ia

from functools import partial
#
# class AssignmentFrame:

#詳細画面クラス
class DetailWindow:
    """
    DetailWindow
        詳細ウィンドウの生成・実行を行うクラス

    --------------
    関数リファレンス

     has_window: 詳細ウィンドウを展開している状態かを返す
            get: subjectインスタンスを返す
    set_subject: subjectインスタンスを設定する
       set_func: 詳細ウィンドウ内のイベント関数を設定する
        set_pos: 詳細ウィンドウの展開位置を設定する
       del_func: 設定されたイベントを削除する
    show_window: 詳細ウィンドウを展開する
    """

    def __init__(self, root, subject = None):
        """
        初期化関数

        Parameters
        -------------
        root : tk.Widget
            親となるwidget
        subject : subjects.subject
            所持するsubjectインスタンス
        """

        self.root = root
        self._win = None
        self._imgs = {}
        self._funcs={}
        self._x = 100
        self._y = 100
        self._colors = { "bg_front":"Medium purple", "bg_back":"grey19", "bg_en":"grey19", "fg_memo_title":"ghostwhite", "en_insertbg":"ghostwhite"}

        tmp = [ "window_closed", "on_restore"]
        for i in tmp:
            self._funcs[i]= ( lambda : {} )

        if subject == None:
            self._subject = sb.Subject()
        else:
            self._subject = subject

    #windowが展開されているかの判定関数
    def has_window(self):
        """
        詳細ウィンドウを作成している状態かを返す

        Returns
        -------------
        if_make_window : Boolean
            作成している => True
            それ以外    => False
        """
        return ( not self._win ==  None and (self._win.winfo_exists()) )

    #subject(科目)のgetter
    def get(self):
        """
        所持しているsubjectインスタンスを取得する

        Returns
        -------------
        subject : subjects.subject
        """
        return self._subject

    #subjectのSetter
    def set_subject(self, subject):
        """
        subjectインスタンスを設定する

        Parameters
        -------------
        subject : subjects.subject
            設定するsubjectインスタンス
        """

        self._subject = subject

    def set_func(self, cmd, func,*args):
        """
        詳細ウィンドウ内のイベント関数を設定する

        Parameters
        -------------
        cmd : String
            設定するイベントの種類を指定する
                window_closed : 詳細ウィンドウを閉じた際のイベント
                on_restore    : 詳細ウィンドウ内の保存ボタンを押した際のイベント
        func : collable
            実行する関数オブジェクト
        *args :
            関数オブジェクトfuncの位置引数

        Example:
        -------------
        func1( x , y):
            print(x+y)
        a, b = 10, 20
        set_func("window_closed", func1, a, b)
            これによって詳細ウィンドウを閉じた際にfunc1関数が呼び出される

        Notes
        -------------
        ・各イベントには一つの関数しか設定できない
        　複数回実行した際は、最後に設定したイベントが呼び出される
        """
        if cmd in self._funcs:
            self._funcs[cmd] = partial(func, *args)
        else:
            print("[Error] 不正なキーワードです。")

    def set_pos(self, x = None, y = None):
        """
        詳細ウィンドウの展開位置を設定する

        Parameters
        -------------
        x: int
            ウィンドウを展開するx座標
        y: int
            ウィンドウを展開するy座標
        """
        if x != None:
            self._x = x
        if y != None:
            self._y = y

    def del_func(cmd):
        """
        設定されたイベントを削除する

        Parameters
        -------------
        cmd : String
            削除するイベントの種類(イベント名はset_funcと同様)
        """
        if cmd in self._funcs:
            del self._funcs[cmd]

    #windowの展開
    def show_window(self, has:tk.BooleanVar = None):
        """
        詳細ウィンドウを作成・展開する

        Parameters
        -------------
        has : tk.BooleanVar
            ウィンドウ展開中はTrueを、ウィンドウ終了後はFalseを示す
            この引数を設定しない場合も、ウィンドウは展開される
        """
        if has == None:
            has = tk.BooleanVar(value=True)

        def _protocol():
            has.set(False)
            self._funcs["window_closed"]()
            self._win.destroy()

        has.set(True)
        if ( not self.has_window() ):
            self._make_window()
        self._win.protocol('WM_DELETE_WINDOW', _protocol )
        self._update()
        self._win.deiconify()


    #windowを展開
    def _make_window(self):

        def _focus_out(*args):
            l_kadai_title.focus()

        if self.has_window():
            self._destory()
        self._win = tk.Toplevel(self.root)
        self._win.withdraw()
        self._win.title("SubWindow")
        self._win.geometry(f"400x700+{self._x}+{self._y}")
        self._win.attributes("-topmost", True)
        self._win.bind("<Destroy>", self._rest_pos, "+")
        #frame設定
        name_frame = tk.Frame(self._win, bg = self._colors["bg_front"], bd = 3, relief = tk.GROOVE, name="name_frame")
        memo_frame = tk.Frame(self._win, bg = self._colors["bg_back"], bd = 5, name="memo_frame")
        commands_frame = tk.Frame(self._win, bg=self._colors["bg_back"],  bd = 3, padx=10, name="commands_frame")
        kadai_frame = tk.Frame(self._win, bg = self._colors["bg_back"], bd = 5, name = "kadai_frame")
        #frame配置
        name_frame.pack( ipadx = 20, fill = tk.X)
        memo_frame.pack( fill = tk.X)
        commands_frame.pack( side=tk.BOTTOM, fill = tk.X, ipadx = 10)
        kadai_frame.pack( expand = True, fill = tk.BOTH)

        #name_frame内
        en_name = cw.GuideEntry(name_frame, font = ("", 15, "bold"), fg="ghostwhite", bg=self._colors["bg_en"], relief=tk.SOLID, insertbackground=self._colors["en_insertbg"], highlightbackground=self._colors["bg_front"], highlightcolor="SteelBlue2", highlightthickness=1, name="en_name")
        en_name.bind("<Return>", _focus_out)
        en_name.set_alpha_color("light sky blue")
        en_name.set_alpha_str("科目名")

        en_name.pack(side=tk.LEFT, expand=True, fill = tk.X, padx = 2)

        #memo_frame内
        self._imgs["l_memo_title"]=tk.PhotoImage(file="./image/detail_window/ico_memo_32_white.png")
        l_memo_title = tk.Label(memo_frame, text="memo", bg = self._colors["bg_back"], fg = self._colors["fg_memo_title"], font = ("Century", 12), image=self._imgs["l_memo_title"], compound="left")
        txb_memo = tk.Text(memo_frame, fg="ghostwhite", bg = self._colors["bg_en"], font=("HGSｺﾞｼｯｸM", 13), height = 6, insertbackground=self._colors["en_insertbg"], bd=1, relief=tk.SOLID, name="txb_memo")

        l_memo_title.pack(side=tk.TOP, anchor=tk.NW, pady = 3, padx = 10)
        txb_memo.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.X, padx = 5, pady= 2)

        #kadai_frame内
        self._imgs["l_kadai_title"]=tk.PhotoImage(file="./image/detail_window/ico_asig_title_32_black.png")
        self._imgs["l_kadai_announce"]=tk.PhotoImage(file="./image/detail_window/ico_announce_16_white.png")
        self._imgs["dummy"]=tk.PhotoImage(file="./image/detail_window/ico_toumei_32.png")
        l_kadai_title = tk.Label(kadai_frame, text="課題一覧", bg = self._colors["bg_front"], fg="grey19", bd=3, font=("HGSｺﾞｼｯｸE", 15), relief = tk.GROOVE, image=self._imgs["l_kadai_title"], compound="left", name="l_kadai_title")
        l_kadai_announce=tk.Label(kadai_frame, text="最近の締め切りは\"2022/6/7\"です", fg="ghostwhite",bg= self._colors["bg_back"], font=("", 10), image=self._imgs["l_kadai_announce"], compound="left", pady=3, name="l_kadai_announce")
        asig_frame=tk.Frame(kadai_frame, bg=self._colors["bg_back"], name="asig_frame")
        sf_kadai= cw.ScrollFrame(asig_frame, name="sf_kadai")

        def _add_asig():
            ias=ia.InputAssignment()

            def _add_widget():
                assignment = ias.get()
                self._subject.add_asg(assignment)
                asi_name = tk.Label(sf_kadai.get(), text=assignment.get_name())
                asi_dead = tk.Label(sf_kadai.get(),
                text=str(assignment.get_deadline()))
                asi_name.pack()
                asi_dead.pack()

            ias.set_func("on_ok_button", _add_widget)
            ias.make_window()
            # tmp = tk.Button(sf_kadai.get(), text="追加された課題", bg="Medium purple1")
            # sf_kadai.pack_widget(tmp, pady=5)

        l_kadai_title.pack(fill = tk.X)
        l_kadai_announce.pack()
        asig_frame.pack( anchor=tk.CENTER, expand=True, fill=tk.Y)
        sf_kadai.pack(side=tk.LEFT,expand=True, fill=tk.Y)

        #保存ボタンの関数
        def _restore():
            name = en_name.get()
            memo = txb_memo.get(1.0, tk.END)
            self._subject.set_name(name)
            self._subject.set_memo(memo)
            self._funcs["on_restore"]()
            _focus_out()

        #commands_frame内
        self._imgs["bt_add_asig"]=tk.PhotoImage(file="./image/detail_window/ico_add_asigh_32_grey.png")
        self._imgs["bt_add_asig_selected"]=tk.PhotoImage(file="./image/detail_window/ico_add_asigh_32_white.png")
        self._imgs["bt_restore"] = tk.PhotoImage(file="./image/detail_window/ico_restore_32_grey.png")
        self._imgs["bt_restore_selected"] = tk.PhotoImage(file="./image/detail_window/ico_restore_32_white.png")
        bt_restore=cw.GuideButton( commands_frame, bg=commands_frame.cget("bg"), fg="ghostwhite", command=_restore, image=self._imgs["bt_restore"], compound="top", bd=0, cursor="hand2", activebackground=commands_frame.cget("bg"))
        bt_restore.config_selected(image=self._imgs["bt_restore_selected"])
        bt_add_asig = cw.GuideButton(commands_frame, bg = "grey19", image=self._imgs["bt_add_asig"], command=_add_asig, bd=0, relief=tk.RAISED, padx=10, cursor="hand2", activebackground=commands_frame.cget("bg"))
        bt_add_asig.config_selected(image=self._imgs["bt_add_asig_selected"])

        # bt_restore_frame.pack(side=tk.LEFT)
        bt_restore.pack(side=tk.LEFT, padx=10)
        bt_add_asig.pack(side=tk.LEFT, padx=10)

    def _update(self):
        name_frame = self._find("name_frame")
        memo_frame = self._find("memo_frame")
        kadai_frame = self._find("kadai_frame")

        en_name=self._find("en_name", name_frame)
        txb_memo=self._find("txb_memo", memo_frame)
        l_kadai_announce=self._find("l_kadai_announce", kadai_frame)
        sf_kadai = self._find("sf_kadai", kadai_frame)

        en_name.insert(self._subject.get_name())
        txb_memo.delete("1.0", "end")
        txb_memo.insert("1.0", self._subject.get_memo())

    #windowの削除
    def _destory(self):
        if self.has_window():
            self._win.destroy()
            self._win = None

    def _rest_pos(self, e=None):
        if self._win != None:
            self._x=self._win.winfo_x()
            self._y=self._win.winfo_y()

    def _find(self, name, widget = None):
        if widget == None:
            if self._win == None:
                return None
            else:
                widget = self._win

        if name in widget.children:
            return widget.nametowidget(name)
        else:
            for v in widget.children.values():
                tmp = self._find(name, v)
                if tmp != None:
                    return tmp
            return None

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Main Window")
    root.geometry("300x300")

    subject = sb.Subject()
    subject.set_name("アルゴリズムとデータ構造")
    subject.set_memo("・レポート提出厳守!")

    dw = DetailWindow(root)
    dw.set_subject(subject)

    def func():
        # subject=dw.get()
        print(dw.get().get_name())
        print("memo:")
        print(dw.get().get_memo())

    def func2():
        tmp = sb.Subject()
        tmp.set_name("最適化2")
        tmp.set_memo("過去問無し、出席点あり")
        dw.set_subject(tmp)
        dw.show_window()
        
    has = tk.BooleanVar(value=True)
    but1 = tk.Button(root, text = "サブウィンドウ表示", command = partial(dw.show_window, has))
    but1.pack()
    but2 = tk.Button(root, text = "Subject取得", command=func)
    but2.pack()
    frame1 = tk.Frame(root)
    but4 = tk.Button(root, text="サブジェクト変更", command=func2)
    but4.pack()


    root.mainloop()
    print(has.get())
