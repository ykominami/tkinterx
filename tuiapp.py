# Textualをインストール: pip install textual
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, RadioSet, RadioButton, Label, Button
from textual.widgets import TextArea
from typing import List, Callable
from info import Info
from client import Client

class TuiApp(App):
    """ラジオボタンとボタンを組み合わせたアプリ"""

    CSS = """
    #options {
        width: 100%;
        height: auto;
        padding: 2;
        border: thick $primary-lighten-2;
    }
    
    RadioButton {
        width: 25%;
        margin: 1;
    }
    """

    def __init__(self, client):
        """初期化メソッド
        
        Args:
            radio_options: ラジオボタンに表示する文字列の配列
            button_options: ボタンに表示する文字列の配列
        """
        super().__init__()
        self.radio_options = client.formats
        self.button_options = client.patterns
        self.client = client
        self.radio_index = 0

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Label("patternを指定してください:")
            with RadioSet(id="options"):
                for i, option in enumerate(self.radio_options):
                    if i == 0:
                        yield RadioButton(f"{option}", value=True)
                    else:
                        yield RadioButton(f"{option}")
            
            # ボタンを横に配置（TextAreaはボタンの上に配置）
            with Vertical():
                # ボタン直下に TextArea を追加（初期値を設定）
                output_area = TextArea(id="output_area")
                output_area.text = "First Text"
                yield output_area

                # ボタン群を横並びにするコンテナ
                with Horizontal():
                    # Exitボタンを追加
                    yield Button("Exit", id="exit_button", variant="error")

                    for i, button_text in enumerate(self.button_options):
                        yield Button(button_text, id=f"button_{i}")
            
            yield Label(id="result")
        yield Footer()

    def on_mount(self) -> None:
        """アプリ起動時の初期化"""
        # デフォルトで最初のオプションを選択
        if self.radio_options:
            self.query_one("#options", RadioSet).value = "0"

        # 初期値の設定は compose 内で行ったためここでは不要

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """ラジオボタンの選択が変更されたとき"""
        selected_radio_text = event.pressed.label
        # eventから選択されたRadioButtonのvalueを取得
        selected_index = event.radio_set.pressed_index
        # selected_value = int( str(selected_label).split(":")[0])
        
        # 選択されたLabelに対応する値をRadioSetの値として設定
        radio_set = self.query_one("#options", RadioSet)
        radio_set.value = selected_index
        
        result_label = self.query_one("#result", Label)
        result_label.update(f"選択中: {selected_radio_text} (値: {selected_index})")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """ボタンが押されたとき"""
        button_id = event.button.id
        
        # Exitボタンがクリックされた場合
        if button_id == "exit_button":
            self.exit()
            return
        
        button_text = event.button.label

        radio_set = self.query_one("#options", RadioSet)
        radio_button = radio_set.pressed_button
        radio_text = radio_button.label
        if radio_text is not None:
            # 文字列化して TextArea にセット
            output_area = self.query_one("#output_area")
            output_area.text = "** Loading ***" # self.client.run の返り値を取得して TextArea に表示
            # event.radio_set.pressed_index
            result_label = self.query_one("#result", Label)
            result_text = str(result_label.render())
            # または、選択状態も含めて表示する場合
            # result_label.update(f"選択中: {selected_option} {selected_value} | {selected_index}| ボタン: {button_text}")
            result_label.update(f"選択中: {result_text} | ボタン: {button_text}")

            try:
                run_result = self.client.run(radio_text, button_text)
            except Exception as e:
                run_result = e

            output_area.text = str(run_result)

if __name__ == "__main__":
    info = Info("info3.json")
    info.load_info()

    # 使用例：文字列配列を渡してアプリを起動
    formats = info.formats
    patterns = info.patterns
    client = Client(formats=formats, patterns=patterns)
    # client.run(client.formats[0], client.patterns[0])
    app = TuiApp(client=client)
    app.run()
