# app/ui/main_ui.py # noqa: E402
import logging
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QTabWidget, QComboBox, QLabel, QMessageBox
from app.ui.initial_settings_tab import InitialSettingsTab # noqa: E402
from app.ui.tabs import CustomTab # noqa: E402
from app.controllers.main_controller import MainController # noqa: E402
from app.ui.left_panel import LeftPanel # noqa: E402

from PyQt5.QtCore import Qt
# ログの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Skill Matrix App")
        self.setGeometry(100, 100, 800, 600)

        # メインウィジェット
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        # メインレイアウト
        self.main_layout = QHBoxLayout(self.main_widget)

        # 左側のレイアウト
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        # タブウィジェット
        self.tab_widget = QTabWidget(self.main_widget)
        self.main_layout.addWidget(self.tab_widget)

        # 初期設定タブ
        self.initial_settings_tab = InitialSettingsTab(controller)
        self.tab_widget.addTab(self.initial_settings_tab, "初期設定")
        
        # グループ選択コンボボックスと参加者リストの配置
        self.left_panel = LeftPanel(controller, self.initial_settings_tab)
        self.left_layout.addWidget(self.left_panel)

        # グループ追加シグナルの接続
        self.initial_settings_tab.group_added.connect(self.on_group_added)
        # 新規タブ追加ボタンのクリックイベント接続
        self.initial_settings_tab.add_tab_button.clicked.connect(self.on_add_tab_clicked)
        
        # データベース接続とビュー更新
        self.setup_left_panel()
        
        self.main_widget.setLayout(self.main_layout)
        logger.debug("MainWindow initialized.")

    def setup_left_panel(self):
        self.left_panel.setup_group_combo()

    def on_add_tab_clicked(self):
        selected_group_name = self.left_panel.group_combo.currentText()
        if not selected_group_name:
            logger.warning("グループが選択されていません")
            QMessageBox.warning(self, "警告", "グループが選択されていません。")
            return
        
        logger.debug(f"Adding new tab for group: {selected_group_name}")
        new_tab = CustomTab(self, selected_group_name)
        self.tab_widget.addTab(new_tab, selected_group_name)

    def on_group_added(self, group_name):
        logger.debug(f"Group added signal received: {group_name}")
        self.setup_left_panel()
