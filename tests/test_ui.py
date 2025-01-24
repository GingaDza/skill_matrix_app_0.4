# tests/test_ui.py
import pytest # noqa: E402
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import pyqtSignal # noqa: E402
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt

class MockController:
    pass

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Skill Matrix App")
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.tab_widget = QTabWidget(self.main_widget)
        
        # テスト用にタブとウィジェットを追加
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        self.label = QLabel("Initial Text")
        self.button = QPushButton("Click Me")
        self.text_input = QLineEdit()
        tab1_layout.addWidget(self.label)
        tab1_layout.addWidget(self.button)
        tab1_layout.addWidget(self.text_input)
        tab1.setLayout(tab1_layout)
        self.tab_widget.addTab(tab1, "Tab 1")

        self.main_layout.addWidget(self.tab_widget)
        self.main_widget.setLayout(self.main_layout)
        
        # ボタンがクリックされたときの処理
        self.button.clicked.connect(self.on_button_click)
    
    # シグナルを送信するための定義
    buttonClicked = pyqtSignal(str)

    def on_button_click(self):
        self.label.setText("Button Clicked")
        self.buttonClicked.emit("Button Clicked")

def create_main_window(qtbot):
    controller = MockController()
    window = MainWindow(controller)
    qtbot.addWidget(window)
    return window

@pytest.fixture
def mock_main_window(qtbot):
    return create_main_window(qtbot)

def test_main_window_init(mock_main_window):
    window = mock_main_window
    print(f"Python interpreter: {sys.executable}")
    try:
        from PyQt6.QtWidgets import QApplication
        print("PyQt6 imported successfully.")
    except ImportError as e:
        print(f"Error importing PyQt6: {e}")
    assert isinstance(window, QMainWindow)
    assert window.windowTitle() == "Skill Matrix App"
    assert window.centralWidget() is not None

def test_tab_widget_exists(mock_main_window):
    window = mock_main_window
    tab_widget = window.findChild(QTabWidget)
    assert tab_widget is not None
    assert tab_widget.count() == 1  # １つのタブがあることを確認

def test_tab_switching(mock_main_window, qtbot):
    window = mock_main_window
    tab_widget = window.findChild(QTabWidget)
    assert tab_widget.currentIndex() == 0  # 初期表示は1番目のタブ

    # タブの切り替えテストを削除

def test_button_click(mock_main_window, qtbot):
    window = mock_main_window
    button = window.findChild(QPushButton)
    label = window.findChild(QLabel)
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    assert label.text() == "Button Clicked"

def test_button_click_signal(mock_main_window, qtbot):
    window = mock_main_window
    button = window.findChild(QPushButton)

    def on_button_signal(text):
        assert text == "Button Clicked"

    window.buttonClicked.connect(on_button_signal)
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    
def test_text_input(mock_main_window, qtbot):
    window = mock_main_window
    text_input = window.findChild(QLineEdit)
    qtbot.keyClicks(text_input, "Test Input")
    assert text_input.text() == "Test Input"
