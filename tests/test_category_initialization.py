import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from app.ui.category_settings import CategorySettings  # noqa: E402

class TestCategorySettingsInitialization(unittest.TestCase):

    @patch('app.ui.category_settings.QMessageBox')  # QMessageBoxクラス全体をモック
    def test_show_error(self, MockQMessageBox):
        # QApplicationのインスタンスを作成
        app = QApplication([])

        # モックされたQMessageBoxのインスタンスを返すように設定
        mock_error_dialog = MagicMock()
        MockQMessageBox.return_value = mock_error_dialog
        
        error_message = "テストエラー"
        
        # CategorySettingsのインスタンスを作成
        category_settings = CategorySettings(None, None)
        
        # show_errorメソッドを呼び出し
        category_settings.show_error(error_message)
        
        # setTextが呼ばれたことを確認
        mock_error_dialog.setText.assert_called_with(error_message)

if __name__ == '__main__':
    unittest.main()
