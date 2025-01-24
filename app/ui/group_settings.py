# app/ui/group_settings.py
import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QLabel, QMessageBox, QDialog
from PyQt5.QtCore import Qt, pyqtSignal  # pyqtSignal をインポート
from app.ui.dialogs import AddCategoryDialog, DeleteConfirmationDialog
from app.models.skill_matrix_model import SkillMatrixModel # SkillMatrixModel をインポート

logger = logging.getLogger(__name__)

class GroupSettings(QWidget):
    group_added = pyqtSignal(str)  # pyqtSignal を使用

    def __init__(self, controller, initial_settings_tab):
        super().__init__()
        logger.debug("Initializing GroupSettings...")
        self.controller = controller
        self.skill_matrix_model = SkillMatrixModel()
        self.initial_settings_tab = initial_settings_tab

        # グループリスト
        self.group_list = QListWidget()

        # ボタンレイアウト
        button_layout = QVBoxLayout()
        self.add_button = QPushButton("新規")
        button_layout.addWidget(self.add_button)
        self.save_button = QPushButton("編集")
        button_layout.addWidget(self.save_button)
        self.delete_button = QPushButton("削除")
        button_layout.addWidget(self.delete_button)

        # メインレイアウト
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("グループ"))
        main_layout.addWidget(self.group_list)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # ボタンのイベント接続
        self.add_button.clicked.connect(self.on_add_group)
        self.save_button.clicked.connect(self.on_save_group)
        self.delete_button.clicked.connect(self.on_delete_group)

        self.load_initial_data()
        logger.debug("GroupSettings Initialized.")

    def load_initial_data(self):
        # ここでskill_matrixを読み込んで処理します
        skill_matrix_list = self.skill_matrix_model.get_skill_matrix()

        groups = []
        for item in skill_matrix_list:
            if item.group and item.group.name not in groups:
                groups.append(item.group.name)

        self.group_list.addItems(groups)

        logger.debug("Groups loaded: %s", groups)

    def on_add_group(self):
        logger.debug("Add group clicked")
        dialog = AddCategoryDialog(self, "新しいグループを追加")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_item = dialog.get_input_text()
            if new_item:
              if self.skill_matrix_model.add_group(new_item):
                  self.group_list.addItem(new_item)
                  self.group_added.emit(new_item)
              else:
                 self.show_error("指定されたグループ名は既に存在します。")
            else:
               self.show_error("グループ名を入力してください。")


    def on_save_group(self):
        logger.debug("Save group clicked")
        selected_item = self.group_list.currentItem()
        if not selected_item:
            self.show_error("編集するグループを選択してください。")
            return

        group_name = selected_item.text()
        dialog = AddCategoryDialog(self, "グループ名を編集", initial_text=group_name)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_group_name = dialog.get_input_text()
            if new_group_name:
                # モデルを呼び出してグループをリネーム
                if self.skill_matrix_model.rename_group(group_name, new_group_name):
                    selected_item.setText(new_group_name)
                    self.initial_settings_tab.update_skill_group_combo()
                else:
                    self.show_error("指定されたグループ名は既に存在します。")

            else:
                self.show_error("グループ名を入力してください。")

    def on_delete_group(self):
      logger.debug("Delete group clicked")
      selected_item = self.group_list.currentItem()
      if not selected_item:
          self.show_error("削除するグループを選択してください。")
          return

      group_name = selected_item.text()
      if QMessageBox.question(self, "削除確認", f"グループ '{group_name}' を削除しますか？") == QMessageBox.StandardButton.Yes:
          if self.skill_matrix_model.delete_group(group_name):
              self.group_list.takeItem(self.group_list.row(selected_item))
              self.initial_settings_tab.update_skill_group_combo()
          else:
              self.show_error("グループの削除に失敗しました。")

    def show_error(self, message):
         logger.error(f"Error: {message}")
         error_dialog = QMessageBox(self)
         error_dialog.setIcon(QMessageBox.Icon.Critical)
         error_dialog.setText(message)
         error_dialog.setWindowTitle("エラー")
         error_dialog.exec()