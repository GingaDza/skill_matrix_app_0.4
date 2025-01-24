import unittest
from PyQt5.QtWidgets import QApplication, QWidget

class TestAppComponents(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # QApplicationを初期化
        cls.app = QApplication([])

    def test_example(self):
        # QWidgetのテスト
        window = QWidget()
        window.setWindowTitle("Test Window")
        self.assertEqual(window.windowTitle(), "Test Window")
        window.show()

if __name__ == "__main__":
    unittest.main()
