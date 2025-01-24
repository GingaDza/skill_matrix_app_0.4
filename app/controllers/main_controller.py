# app/controllers/main_controller.py # noqa: E402
from PyQt5.QtWidgets import QPushButton

class MainController:
    def __init__(self, window):
        self.window = window  # MainWindowオブジェクトを受け取る
        print("MainController initialized")

    def setup_ui(self):
        # window（MainWindowオブジェクト）のボタンを追加する
        button = QPushButton("Click Me (from Controller)", self.window)
        button.clicked.connect(self.on_button_click)

        # ボタンをウィンドウに追加
        layout = self.window.centralWidget().layout()  # 既存のレイアウトを取得
        layout.addWidget(button)

    def on_button_click(self):
        print("Button clicked from controller!")
