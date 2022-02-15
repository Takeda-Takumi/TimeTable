import tkinter as tk
import tkinter.font as f
import subject as sb

#スクロールすることができるフレーム
class ScrolFrame(tk.Frame):

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

#詳細画面クラス
#DetailWindowの展開はshow_window関数
#Subjectの取得はget関数
class DetailWindow:

    def __init__(self, root, subject = None):
        self.root = root
        self._win = None
        self._imgs = {}
        self._colors = { "bg_front":"Medium purple1", "bg_back":"grey19", "bg_en":"grey19", "fg_memo_title":"ghostwhite", "en_insertbg":"ghostwhite"}

        self.list=[]

        if subject == None:
            self._subject = sb.Subject()
        else:
            self._subject = subject

    #windowが展開されているかの判定関数
    def has_window(self):
        return ( not self._win ==  None and (self._win.winfo_exists()) )

    #subject(科目)のgetter
    def get(self):
        return self._subject

    #subjectのSetter
    def set_subject(self, subject):
        self._subject = subject

    #windowの展開
    def show_window(self):
        self._make_window()
        self._win.deiconify()

    #windowを展開
    def _make_window(self):
        if self.has_window():
            self._destory()
        self._win = tk.Toplevel(self.root)
        self._win.withdraw()
        self._win.title("SubWindow")
        self._win.geometry(f"400x700+100+100")
        self._win.attributes("-topmost", True)

        #frame設定
        name_frame = tk.Frame(self._win, bg = self._colors["bg_front"], bd = 3, relief = tk.GROOVE)
        memo_frame = tk.Frame(self._win, bg = self._colors["bg_back"], bd = 5)
        commands_frame = tk.Frame(self._win, bg=self._colors["bg_front"],  bd = 3)
        kadai_frame = tk.Frame(self._win, bg = self._colors["bg_back"], bd = 5)

        #frame配置
        name_frame.pack( ipadx = 20, fill = tk.X)
        memo_frame.pack( fill = tk.X)
        commands_frame.pack( side=tk.BOTTOM, fill = tk.X)
        kadai_frame.pack( expand = True, fill = tk.BOTH)
        # commands_frame.pack( side=tk.BOTTOM, expand = True, fill = tk.BOTH, ipadx = 3)

        #name_frame内
        l_title = tk.Label(name_frame, text="科目名", bg = self._colors["bg_front"], font = ("", 15, "bold"))
        en_name = tk.Entry(name_frame, font = ("", 15, "bold"), fg="ghostwhite", bg=self._colors["bg_en"], relief=tk.SOLID, insertbackground=self._colors["en_insertbg"], highlightbackground=self._colors["bg_front"], highlightcolor="SteelBlue2", highlightthickness=3)
        en_name.insert(0, self._subject.get_name())

        l_title.pack(side=tk.LEFT, padx = 5, pady=3)
        en_name.pack(side=tk.LEFT, expand=True, fill = tk.X, padx = 2)

        #memo_frame内
        self._imgs["l_memo_title"]=tk.PhotoImage(file="./image/detail_window/ico_memo_32_white.png")
        l_memo_title = tk.Label(memo_frame, text="memo", bg = self._colors["bg_back"], fg = self._colors["fg_memo_title"], font = ("Century", 12), image=self._imgs["l_memo_title"], compound="left")
        txb_memo = tk.Text(memo_frame, fg="ghostwhite", bg = self._colors["bg_en"], font=("HGSｺﾞｼｯｸM", 13), height = 6, insertbackground=self._colors["en_insertbg"], bd=3)
        txb_memo.insert(tk.END, self._subject.get_memo())

        l_memo_title.pack(side=tk.TOP, anchor=tk.NW, pady = 3, padx = 10)
        txb_memo.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.X, padx = 5, pady= 2)

        #kadai_frame内
        self._imgs["l_kadai_title"]=tk.PhotoImage(file="./image/detail_window/ico_asig_title_32_black.png")
        self._imgs["l_kadai_announce"]=tk.PhotoImage(file="./image/detail_window/ico_announce_16_white.png")
        self._imgs["bt_add_asig"]=tk.PhotoImage(file="./image/detail_window/ico_add_asig_32_white.png")
        self._imgs["dummy"]=tk.PhotoImage(file="./image/detail_window/ico_toumei_32.png")
        l_kadai_title = tk.Label(kadai_frame, text="課題一覧", bg = self._colors["bg_front"], fg="grey19", bd=3, font=("HGSｺﾞｼｯｸE", 15), relief = tk.GROOVE, image=self._imgs["l_kadai_title"], compound="left")
        l_kadai_announce=tk.Label(kadai_frame, text="最近の締め切りは\"2022/6/7\"です", fg="ghostwhite",bg= self._colors["bg_back"], font=("", 10), image=self._imgs["l_kadai_announce"], compound="left", pady=3)
        asig_frame=tk.Frame(kadai_frame, bg=self._colors["bg_back"])
        sf_kadai= ScrolFrame(asig_frame)

        def _add_asig():
            tmp = tk.Button(sf_kadai.get(), text="追加された課題", bg="Medium purple1")
            sf_kadai.pack_widget(tmp, pady=5)

        bt_dummy = tk.Button(asig_frame, bg = self._colors["bg_back"], image=self._imgs["dummy"], bd=0,state="disable")
        bt_add_asig = tk.Button(asig_frame, bg = "grey19", image=self._imgs["bt_add_asig"], command=_add_asig, bd=3, relief=tk.RAISED)

        l_kadai_title.pack(fill = tk.X)
        l_kadai_announce.pack()
        asig_frame.pack( anchor=tk.CENTER, expand=True, fill=tk.Y)
        bt_dummy.pack(side=tk.LEFT, anchor=tk.N)
        sf_kadai.pack(side=tk.LEFT,expand=True, fill=tk.Y)
        bt_add_asig.pack(side=tk.LEFT, anchor=tk.N, pady=5)

        #保存ボタンの関数
        def _restore():
            name = en_name.get()
            memo = txb_memo.get(1.0, tk.END)
            self._subject.set_name(name)
            self._subject.set_memo(memo)
            _focus_out()

        def _focus_out():
            l_kadai_title.focus()

        #commands_frame内
        self._imgs["bt_restore"] = tk.PhotoImage(file="./image/detail_window/ico_restore_32_white.png")
        bt_restore_frame=tk.Frame( commands_frame, bg = "black", relief=tk.RAISED, pady = 3, padx=3, bd=4)
        bt_restore=tk.Button(bt_restore_frame, text="保存", bg="black", fg="ghostwhite", command=_restore, image=self._imgs["bt_restore"], compound="top", bd=0)

        bt_restore_frame.pack(side=tk.LEFT)
        bt_restore.pack()

    #windowの削除
    def _destory(self):
        if self.has_window():
            self._win.destroy()
            self._win = None

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Main Window")
    root.geometry("1000x600")

    subject = sb.Subject()
    subject.set_name("アルゴリズムとデータ構造")
    subject.set_memo("・レポート提出厳守!")

    dw = DetailWindow(root)
    dw.set_subject(subject)

    def func():
        subject=dw.get()
        print(subject.get_name())
        print("memo:")
        print(subject.get_memo())

    but1 = tk.Button(root, text = "サブウィンドウ表示", command = dw.show_window)
    but1.pack()
    but2 = tk.Button(root, text = "Subject取得", command=func)
    but2.pack()
    root.mainloop()
