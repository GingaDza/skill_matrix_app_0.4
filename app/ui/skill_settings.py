# app/ui/skill_settings.py
import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout,  QLabel, QListWidget, QPushButton, QComboBox, QMessageBox, QDialog
from PyQt5.QtCore import Qt
from app.ui.dialogs import EditSkillDialog, DeleteConfirmationDialog
from app.models.skill_matrix_model import SkillMatrixModel # SkillMatrixModel をインポート
from typing import Optional

logger = logging.getLogger(__name__)

class SkillSettings(QWidget):
    def __init__(self, controller,initial_settings_tab): # initial_settings_tab を追加
        super().__init__()
        logger.debug("Initializing SkillSettings...")
        self.controller = controller
        self.skill_matrix_model = SkillMatrixModel()
        self.initial_settings_tab = initial_settings_tab # ここで設定

        # スキルレベルリスト
        self.skill_level_list = QListWidget()
        # スキルレベルコンボボックス
        self.skill_group_combo = QComboBox() # グループ選択コンボボックスを追加
        self.skill_level_combo = QComboBox()
        self.skill_level_combo.addItems([str(i) for i in range(1, 11)]) # 1から10までのコンボボックス
        self.skill_level_combo.setCurrentText("1")

        # スキルレベル操作ボタン
        self.skill_add_button = QPushButton("反映")
        self.skill_save_button = QPushButton("編集")
        self.skill_delete_button = QPushButton("削除")

        skill_layout = QVBoxLayout()
        skill_layout.addWidget(QLabel("スキルレベル"))
        skill_layout.addWidget(self.skill_group_combo)  # スキルグループコンボボックスを追加
        skill_layout.addWidget(self.skill_level_combo)
        skill_layout.addWidget(self.skill_add_button)
        skill_layout.addWidget(self.skill_save_button)
        skill_layout.addWidget(self.skill_delete_button)
        skill_layout.addWidget(self.skill_level_list)

        main_layout = QVBoxLayout()
        main_layout.addLayout(skill_layout)
        self.setLayout(main_layout)

         # ボタンのイベント接続
        self.skill_add_button.clicked.connect(self.on_add_skill)
        self.skill_save_button.clicked.connect(self.on_save_skill)  # スキル編集ボタンの接続
        self.skill_delete_button.clicked.connect(self.on_delete_skill)
        
        self.skill_group_combo.currentIndexChanged.connect(self.update_skill_level_list) # スキルグループコンボボックスのイベント接続
        logger.debug("SkillSettings Initialized.")
        self.setup_group_combo()
    
    def _get_selected_skill_info(self) -> tuple[Optional[str], Optional[str], Optional[str]]:
        selected_group_name = self.skill_group_combo.currentText()
        selected_parent = self.initial_settings_tab.category_settings.parent_category_list.currentItem()
        selected_child = self.initial_settings_tab.category_settings.child_category_list.currentItem()
        return (
            selected_group_name,
            self._get_text_or_none(selected_parent),
            self._get_text_or_none(selected_child),
        )

    def _get_text_or_none(self, item) -> Optional[str]:
        return item.text() if item else None

    def on_add_skill(self):
        logger.debug("Triggered: Add skill")
        selected_group_name, selected_parent, selected_child = self._get_selected_skill_info()
        if not selected_group_name:
            self.show_error("グループを選択してください。")
            return

        logger.debug(f"Adding skill for group: {selected_group_name}")
        
        try:
          new_skill_level = int(self.skill_level_combo.currentText())
        except ValueError:
           self.show_error("無効なスキルレベルが選択されました。")
           return
        
        skill_levels_to_add = list(range(1, new_skill_level + 1))
        
        if selected_parent and selected_child:
            parent_name = selected_parent
            child_name = selected_child
            for level in skill_levels_to_add:
                 self.skill_matrix_model.add_skill(selected_group_name, parent_name , child_name, level)
        else:
            for level in skill_levels_to_add:
                self.skill_matrix_model.add_skill(selected_group_name, None, None, level)
        self.update_skill_level_list()

    def on_save_skill(self):
        logger.debug("Save skill clicked")
        selected_items = self.skill_level_list.selectedItems()
        if not selected_items:
            self.show_error("編集するスキルを選択してください。")
            return

        selected_group_name, selected_parent, selected_child = self._get_selected_skill_info()
        if not selected_group_name:
            return

        skill_name_with_value = selected_items[0].text()
        skill_name = skill_name_with_value.split(": ")[0]

        # スキル編集用のダイアログを表示
        dialog = EditSkillDialog(self, "スキルを編集", skill_name)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_skill_level = dialog.get_skill_level()
            if self.skill_matrix_model.rename_skill(selected_group_name,
                                                    selected_parent,
                                                    selected_child,
                                                    int(skill_name), new_skill_level):
                self.update_skill_level_list()
            else:
                self.show_error("スキルの編集に失敗しました。")

    def on_delete_skill(self):
        logger.debug("Delete skill clicked")
        selected_items = self.skill_level_list.selectedItems()
        if not selected_items:
            self.show_error("削除するスキルレベルを選択してください。")
            return
        delete_dialog = DeleteConfirmationDialog(self, "削除確認", "本当に削除しますか？")
        if delete_dialog.exec() == QDialog.DialogCode.Accepted:
            selected_group_name, selected_parent, selected_child = self._get_selected_skill_info()
            if not selected_group_name:
                return

            for item in selected_items:
                skill_level = item.text().split(": ")[0]
                try:
                    skill_level = int(skill_level)
                except ValueError:
                    logger.error(f"Invalid skill level format: {skill_level}")
                    continue
                if self.skill_matrix_model.delete_skill(selected_group_name,
                                                        selected_parent,
                                                        selected_child,
                                                        skill_level):
                    self.skill_level_list.takeItem(self.skill_level_list.row(item))
                else:
                    self.show_error("スキルの削除に失敗しました")

    def update_skill_level_list(self, current=None, previous=None):
        self.skill_level_list.clear()
        selected_group_name, selected_parent, selected_child = self._get_selected_skill_info()

        logger.debug(f"Updating skill level list for group: {selected_group_name}, parent: {selected_parent}, child: {selected_child}")
        
        # InitialSettingsTab の fetch_skill_levels メソッドを利用する
        if not selected_group_name:
            logger.debug("No group selected to update skill level list.")
            return
        
        skill_levels_to_display = self.initial_settings_tab.fetch_skill_levels(selected_group_name, selected_parent, selected_child)
        self._populate_skill_level_list(skill_levels_to_display)

    def _populate_skill_level_list(self, skill_levels):
        max_skill_level = 0
        for level in skill_levels:
            self.skill_level_list.addItem(str(level))
            try:
                max_skill_level = max(max_skill_level, int(level))
            except ValueError as e:
                logger.warning(f"Invalid skill level format: {level}, error: {e}")
        if max_skill_level > 0:
            self.skill_level_combo.setCurrentText(str(max_skill_level))
        else:
            self.skill_level_combo.setCurrentText("1")

    def setup_group_combo(self):
      try:
        skill_matrix = self.initial_settings_tab.skill_matrix_model.get_skill_matrix()
        groups = {item.group.name for item in skill_matrix if item.group}
        if not groups:
            self.show_error("利用可能なグループがありません。新しいグループを追加してください。")
            return
        self.skill_group_combo.addItems(groups)
        self.skill_group_combo.currentIndexChanged.connect(self.update_skill_level_list)
      except Exception as e:
            logger.error(f"setup_group_combo: {e}")
            self.show_error("setup_group_combo: グループコンボボックスの初期設定に失敗しました。")

    def show_error(self, message):
         logger.error(f"Error: {message}")
         error_dialog = QMessageBox(self)
         error_dialog.setIcon(QMessageBox.Icon.Critical)
         error_dialog.setText(message)
         error_dialog.setWindowTitle("エラー")
         error_dialog.exec()