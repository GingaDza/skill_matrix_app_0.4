# main.py
import sys
from PyQt5.QtWidgets import QApplication
from app.ui.main_ui import MainWindow  # main_ui.py から MainWindow をインポート
from app.controllers.main_controller import MainController
from app.logger import logger #loggerのimport

if __name__ == "__main__":
    logger.debug("Starting Application...")
    app = QApplication(sys.argv)
    
    # スタイルシートの適用
    with open("static/styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow(MainController(None)) # UIの表示処理はMainWindow内で行う
    window.show()
    sys.exit(app.exec_())