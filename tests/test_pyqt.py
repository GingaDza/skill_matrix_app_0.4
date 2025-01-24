from PyQt5.QtWidgets import QApplication

try:
    app = QApplication([])
except Exception as e:
    assert False, f"PyQt5 is not installed: {e}"
