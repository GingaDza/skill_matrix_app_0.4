import logging
from PyQt5.QtWidgets import QMessageBox, QLabel, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton
from app.ui.dialogs import AddCategoryDialog, DeleteConfirmationDialog
from app.models.skill_matrix_model import SkillMatrixModel

logger = logging.getLogger(__name__)

class CategorySettings(QWidget):
    def __init__(self, controller, initial_settings_tab):
        super().__init__()
        logger.debug("Initializing CategorySettings...")
        self.controller = controller
        self.skill_matrix_model = SkillMatrixModel()
        self.initial_settings_tab = initial_settings_tab

        # 親カテゴリーリスト
        self.parent_category_list = QListWidget()
        # ボタンレイアウト（親カテゴリー）
        parent_button_layout = QVBoxLayout()
        self.parent_add_button = QPushButton("新規")
        parent_button_layout.addWidget(self.parent_add_button)
        self.parent_save_button = QPushButton("編集")
        parent_button_layout.addWidget(self.parent_save_button)
        self.parent_delete_button = QPushButton("削除")
        parent_button_layout.addWidget(self.parent_delete_button)
        # 親カテゴリー
        parent_layout = QVBoxLayout()
        parent_layout.addWidget(QLabel("親カテゴリー"))
        parent_layout.addWidget(self.parent_category_list)
        parent_layout.addLayout(parent_button_layout)

        # 子カテゴリーリスト
        self.child_category_list = QListWidget()
        # ボタンレイアウト（子カテゴリー）
        child_button_layout = QVBoxLayout()
        self.child_add_button = QPushButton("新規")
        child_button_layout.addWidget(self.child_add_button)
        self.child_save_button = QPushButton("編集")
        child_button_layout.addWidget(self.child_save_button)
        self.child_delete_button = QPushButton("削除")
        child_button_layout.addWidget(self.child_delete_button)
        # 子カテゴリー
        child_layout = QVBoxLayout()
        child_layout.addWidget(QLabel("子カテゴリー"))
        child_layout.addWidget(self.child_category_list)
        child_layout.addLayout(child_button_layout)

        main_layout = QHBoxLayout()
        main_layout.addLayout(parent_layout)
        main_layout.addLayout(child_layout)
        self.setLayout(main_layout)

        # 親カテゴリーのボタンのイベント接続
        self.parent_add_button.clicked.connect(self.on_add_parent)
        self.parent_save_button.clicked.connect(self.on_save_parent)
        self.parent_delete_button.clicked.connect(self.on_delete_parent)
        # 子カテゴリーのボタンのイベント接続
        self.child_add_button.clicked.connect(self.on_add_child)
        self.child_save_button.clicked.connect(self.on_save_child)
        self.child_delete_button.clicked.connect(self.on_delete_child)
        logger.debug("CategorySettings Initialized.")

    def show_error(self, message):
        logger.error(f"Error: {message}")
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText(message)  # ここでsetTextを呼んでいる
        error_dialog.setWindowTitle("エラー")
        error_dialog.setInformativeText(message)
        error_dialog.exec()

    def on_add_parent(self):
        logger.debug("Add parent clicked")
        selected_group = self.initial_settings_tab.group_settings.group_list.currentItem()
        if not selected_group:
            self.show_error("グループを選択してください。")
            return

        group_name = selected_group.text()
        logger.debug(f"Selected group: {group_name}")

        # 親カテゴリが初期化されているか確認
        if not self.skill_matrix_model.is_parent_category_initialized(group_name):
            logger.error(f"Parent category for group {group_name} is not initialized.")
            self.show_error("親カテゴリーが初期化されていません。")
            return

        dialog = AddCategoryDialog(self, "新しい親カテゴリーを追加")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_item = dialog.get_input_text()
            if new_item:
                if self.skill_matrix_model.add_parent_category(group_name, new_item):
                    self.parent_category_list.addItem(new_item)
                    self.initial_settings_tab.update_parent_list(self.initial_settings_tab.group_settings.group_list.currentItem(), None)
                    logger.debug(f"Parent category '{new_item}' added successfully.")
                else:
                    logger.error(f"Failed to add parent category '{new_item}' for group '{group_name}'.")
                    self.show_error("親カテゴリー名は既に存在します。")
            else:
                self.show_error("親カテゴリー名が無効です。")

    def on_save_parent(self):
        logger.debug("Save parent clicked")
        selected_item = self.parent_category_list.currentItem()
        if not selected_item:
            self.show_error("編集する親カテゴリーを選択してください。")
            return

        parent_name = selected_item.text()
        dialog = AddCategoryDialog(self, "親カテゴリー名を編集", initial_text=parent_name)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_parent_name = dialog.get_input_text()
            if new_parent_name:
                group_name = self.initial_settings_tab.group_settings.group_list.currentItem().text()
                if self.skill_matrix_model.rename_parent_category(group_name, parent_name, new_parent_name):
                    selected_item.setText(new_parent_name)
                    self.initial_settings_tab.update_parent_list(self.initial_settings_tab.group_settings.group_list.currentItem(), None)
                else:
                    self.show_error("親カテゴリー名が無効、または既に存在します。")
            else:
                self.show_error("親カテゴリー名を入力してください。")

    def on_delete_parent(self):
        logger.debug("Delete parent clicked")
        selected_item = self.parent_category_list.currentItem()
        if not selected_item:
            self.show_error("削除する親カテゴリーを選択してください。")
            return

        parent_name = selected_item.text()
        if QMessageBox.question(self, "削除確認", f"親カテゴリー '{parent_name}' を削除しますか？") == QMessageBox.StandardButton.Yes:
            group_name = self.initial_settings_tab.group_settings.group_list.currentItem().text()
            if self.skill_matrix_model.delete_parent_category(group_name, parent_name):
                self.parent_category_list.takeItem(self.parent_category_list.row(selected_item))
                self.child_category_list.clear()
                self.initial_settings_tab.skill_settings.skill_level_list.clear()
                self.initial_settings_tab.update_parent_list(self.initial_settings_tab.group_settings.group_list.currentItem(), None)
            else:
                self.show_error("親カテゴリーの削除に失敗しました")

    def on_add_child(self):
        logger.debug("Add child clicked")
        selected_parent = self.parent_category_list.currentItem()
        selected_group = self.initial_settings_tab.group_settings.group_list.currentItem()

        if not selected_parent:
            self.show_error("親カテゴリーを選択してください")
            return
        if not selected_group:
            self.show_error("グループを選択してください")
            return

        group_name = selected_group.text()
        parent_name = selected_parent.text()

        dialog = AddCategoryDialog(self, "新しい子カテゴリーを追加")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_item = dialog.get_input_text()
            if new_item:
                if self.skill_matrix_model.add_child_category(group_name, parent_name, new_item):
                    self.initial_settings_tab.update_child_categories(selected_parent, None)
                else:
                    self.show_error("子カテゴリー名は既に存在します。")
            else:
                self.show_error("空の子カテゴリー名を入力しないでください。")

    def on_save_child(self):
        logger.debug("Save child clicked")
        selected_item = self.child_category_list.currentItem()
        if not selected_item:
            self.show_error("編集する子カテゴリーを選択してください。")
            return

        child_name = selected_item.text()
        dialog = AddCategoryDialog(self, "子カテゴリー名を編集", initial_text=child_name)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_child_name = dialog.get_input_text()
            if new_child_name:
                group_name = self.initial_settings_tab.group_settings.group_list.currentItem().text()
                parent_name = self.parent_category_list.currentItem().text()
                if self.skill_matrix_model.rename_child_category(group_name, parent_name, child_name, new_child_name):
                    selected_item.setText(new_child_name)
                    self.initial_settings_tab.update_child_categories(selected_item, None)
                else:
                    self.show_error("指定された子カテゴリー名は既に存在します。")
            else:
                self.show_error("子カテゴリー名を入力してください。")

    def on_delete_child(self):
        logger.debug("Delete child clicked")
        selected_items = self.child_category_list.selectedItems()
        if not selected_items:
            self.show_error("削除する子カテゴリーを選択してください。")
            return
        delete_dialog = DeleteConfirmationDialog(self, "削除確認", "本当に削除しますか？")
        if delete_dialog.exec() == QDialog.DialogCode.Accepted:
            selected_parent = self.parent_category_list.currentItem()
            selected_group = self.initial_settings_tab.group_settings.group_list.currentItem()
            if selected_group and selected_parent:
                group_name = selected_group.text()
                parent_name = selected_parent.text()
                for item in selected_items:
                    child_name = item.text()
                    if self.skill_matrix_model.delete_child_category(group_name, parent_name, child_name):
                        self.child_category_list.takeItem(self.child_category_list.row(item))
                        self.initial_settings_tab.update_child_categories(selected_parent, None)
                    else:
                        self.show_error("子カテゴリーの削除に失敗しました")

    def add_subcategory(self, subcategory_name):
        """仮のメソッドで子カテゴリーを追加する"""
        self.child_category_list.addItem(subcategory_name)
