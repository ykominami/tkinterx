import tkinter as tk
from typing import List, Callable
from info import Info
from client import Client

class GuiApp():
    """
    文字列のリストから縦一列のボタン群を生成し、
    クリックされたボタンの文字列を返す機能を持つクラス。
    """
    def __init__(self, client):
        """初期化メソッド
        
        Args:
            radio_options: ラジオボタンに表示する文字列の配列
            button_options: ボタンに表示する文字列の配列
        """
        # super().__init__()
        self.client = client
        self.format_list = client.formats
        self.pattern_list = client.patterns
        self.format = None
        self.pattern = None
        self.callback = None

    def run(self):
        # 1. ボタンがクリックされたときに実行する関数を定義
        def handle_button_click(clicked_string: str):
            """
            コールバック関数。クリックされたボタンの文字列を受け取り、
            コンソールとウィンドウのラベルに表示する。
            """
            print(f"ボタン '{clicked_string}' がクリックされました！")
            # ウィンドウ下部のラベルのテキストを更新（ラベルがまだない場合はスキップ）
            lbl = getattr(self, 'result_label', None)
            if lbl is not None:
                lbl.config(text=f"選択された項目: {clicked_string}")
            self.pattern = clicked_string
            # 呼び出しの戻り値を取得してTextAreaに表示する
            try:
                result = self.client.run(format_option=self.format, pattern_option=self.pattern)
            except Exception as e:
                result = f"Error: {e}"

            # TextArea がまだ作られていない場合は無視
            try:
                # 既存の内容をクリアしてから結果を挿入
                self.text_area.delete('1.0', tk.END)
                # 非文字列でも扱えるように変換
                self.text_area.insert(tk.END, str(result))
            except Exception:
                pass

        # 2. ラジオボタンが選択されたときに実行する関数を定義
        def handle_radio_selection(selected_string: str):
            """
            ラジオボタン選択時のコールバック関数。
            """
            print(f"ラジオボタン '{selected_string}' が選択されました！")
            lbl = getattr(self, 'radio_result_label', None)
            if lbl is not None:
                lbl.config(text=f"選択されたラジオボタン: {selected_string}")
            self.format = selected_string

        self.callback = handle_button_click
        self.radio_callback = handle_radio_selection

        # 3. メインのウィンドウを作成
        root = tk.Tk()
        root.title("文字列リストからのボタン生成 + ラジオボタン")
        root.geometry("300x500") # ウィンドウの初期サイズ

        # 4. ボタンにしたい文字列のリストを定義
        self.pattern_list = self.client.patterns
        self.pattern = self.pattern_list[0]
        # 5. ラジオボタンにしたい文字列のリストを定義
        self.format_list = self.client.formats
        self.format = self.format_list[0]

        ####################################
        # ボタンをまとめるためのキャンバスとコンテナを作成
        # 横に並んだボタンを折返さず、ウィンドウ幅を超える場合はスクロール可能にする
        self.button_canvas = tk.Canvas(root, height=40)
        self.button_scrollbar = tk.Scrollbar(root, orient='horizontal', command=self.button_canvas.xview)
        self.button_canvas.configure(xscrollcommand=self.button_scrollbar.set)
        self.button_container = tk.Frame(self.button_canvas)
        self.button_canvas.create_window((0, 0), window=self.button_container, anchor='nw')
        # コンテナのサイズ変化でスクロール領域を更新
        self.button_container.bind("<Configure>", lambda e: self.button_canvas.configure(scrollregion=self.button_canvas.bbox("all")))

        # ラジオボタン用のフレームを作成（先に配置する）
        self.radio_frame = tk.Frame(root)

        self.selected_pattern = None
        self.selected_format = None
        # ラジオボタン用の変数
        self.radio_var = tk.StringVar()

        # ラジオボタンを先に生成して配置する
        if self.format_list:
            self.radio_frame.pack(pady=10, padx=10)
            self._create_radio_buttons()

        # TextArea（ラジオボタンとボタンの間に表示）を作成
        self.text_area = tk.Text(root, height=8, wrap='word')
        self.text_area.pack(fill='both', expand=False, pady=5, padx=10)

        # ボタン用のキャンバスとスクロールバーを配置してからボタン群を生成（先頭に Exit ボタン）
        self.button_canvas.pack(fill='x', padx=10, pady=5)
        self.button_scrollbar.pack(fill='x', padx=10)
        exit_button = tk.Button(self.button_container, text="Exit", fg="white", bg="red", command=root.destroy)
        exit_button.pack(side='left', padx=2, pady=2)
        self._create_buttons()

        # 結果を表示するためのラベルをウィンドウに配置
        self.result_label = tk.Label(root, text="上のボタンをクリックしてください", font=("Helvetica", 12))
        self.result_label.pack(pady=10)
        
        # ラジオボタンの結果を表示するためのラベルをウィンドウに配置
        self.radio_result_label = tk.Label(root, text="ラジオボタンを選択してください", font=("Helvetica", 12))
        self.radio_result_label.pack(pady=10)

        # アプリケーションのメインループを開始
        root.mainloop()

    

    def _create_buttons(self):
        """
        リストの各要素に対応するボタンを生成して、フレーム内に縦一列に配置する。
        """
        print("ボタンを生成します...")
        for item_text in self.pattern_list:
            # 各ボタンにcommandとしてlambda関数を割り当てる
            # これにより、どのボタンが押されたかを区別できる
            #
            # 重要: `t=item_text` のようにデフォルト引数を使うことで、
            #       ループの各時点でのitem_textの値を正しくボタンに束縛できる。
            # Buttons are created inside button_container so they can scroll horizontally
            
            # ボタンをフレーム内に配置する (packはデフォルトで縦に並べる)
            # fill='x'でボタンの幅をフレームの幅に合わせ、padyで上下に少し余白を作る
            button = tk.Button(
                self.button_container,
                text=item_text,
                command=lambda t=item_text: self.callback(t)
            )
            button.pack(side='left', padx=2, pady=2)

    def _wrap_buttons(self):
        """
        フレーム幅に合わせてボタンを左から順に並べ、幅を超えたら折り返す
        """
        # 既存の配置をクリア
        for w in self.frame.winfo_children():
            w.grid_forget()

        if not self.buttons:
            return

        # 利用可能な幅を取得
        total_width = self.frame.winfo_width()
        if total_width <= 1:
            # 初期状態では幅が正しく取れないことがあるので遅延実行
            self.frame.after(100, self._wrap_buttons)
            return

        x = 0  # 現在行の使用ピクセル幅
        row = 0
        col = 0  # grid のカラムインデックス
        padding = 4
        for btn in self.buttons:
            btn.update_idletasks()
            w = btn.winfo_reqwidth() + padding
            # 幅を超える場合は折り返し
            if x + w > total_width and x > 0:
                row += 1
                col = 0
                x = 0
            # ボタンを grid に配置
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='w')
            # 次の位置を更新
            x += w
            col += 1

    def _create_radio_buttons(self):
        """
        ラジオボタンオプションの各要素に対応するラジオボタンを生成して配置する。
        """
        print("ラジオボタンを生成します...")
        
        # ラジオボタンのタイトルラベル
        title_label = tk.Label(self.radio_frame, text="選択してください:", font=("Helvetica", 10, "bold"))
        title_label.pack(anchor='w')
        
        for i, option_text in enumerate(self.format_list):
            radio_button = tk.Radiobutton(
                self.radio_frame,
                text=option_text,
                variable=self.radio_var,
                value=option_text,
                command=lambda: self._on_radio_selected()
            )
            radio_button.pack(anchor='w', pady=1)
        
        # デフォルトで最初のオプションを選択
        if self.format_list:
            self.selected_format = self.format_list[0]
            self.radio_var.set(self.selected_format)

    def _on_radio_selected(self):
        """
        ラジオボタンが選択されたときのコールバック
        """
        selected_value = self.radio_var.get()
        if self.radio_callback:
            self.radio_callback(selected_value)

    def get_selected_radio(self) -> str:
        """
        現在選択されているラジオボタンの値を取得
        """
        return self.radio_var.get()


# --- ここから下は、このクラスを実際に使うためのサンプルコード ---

if __name__ == "__main__":
    info = Info("info3.json")
    info.load_info()

    # 使用例：文字列配列を渡してアプリを起動
    formats = info.formats
    patterns = info.patterns
    client = Client(formats=formats, patterns=patterns)

    app = GuiApp(client=client)
    app.run()

