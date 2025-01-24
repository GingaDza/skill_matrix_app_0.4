# app/ui/initial_settings_tab.py
import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal  # ここでpyqtSignalをインポート
from typing import Optional, Tuple
from PyQt5.QtCore import QTimer

# 遅延インポートを適用
class InitialSettingsTab(QWidget):
    initialized = pyqtSignal()
    group_added = pyqtSignal(str)

    def __init__(self, controller, skill_matrix_model=None):
        super().__init__()
        logging.debug("Initializing InitialSettingsTab...")

        self.controller = controller
        self.skill_matrix_model = skill_matrix_model or self._import_skill_matrix_model()

        # UI要素を分割
        self.group_settings = self._import_group_settings()
        self.category_settings = self._import_category_settings()
        self.skill_settings = self._import_skill_settings()

        # SkillSettings に self を渡して初期化
        self.skill_settings.initial_settings_tab = self

        # 新規タブ追加ボタン
        self.add_tab_button = QPushButton("新規タブ追加")

        # メインレイアウト
        main_layout = QVBoxLayout()

        # 横並びレイアウト
        list_layout = QHBoxLayout()
        list_layout.addWidget(self.group_settings)
        list_layout.addWidget(self.category_settings)
        list_layout.addWidget(self.skill_settings)
        main_layout.addLayout(list_layout)
        main_layout.addWidget(self.add_tab_button)
        
        self.setLayout(main_layout)

        # シグナル接続
        QTimer.singleShot(100, self.setup_signals) # 100ms後に実行

        logging.debug("InitialSettingsTab initialized.")
        self.initialized.emit()
    
    def _import_skill_matrix_model(self):
        from app.models.skill_matrix_model import SkillMatrixModel
        return SkillMatrixModel()

    def _import_group_settings(self):
        from app.ui.group_settings import GroupSettings
        return GroupSettings(self.controller, self)

    def _import_category_settings(self):
        from app.ui.category_settings import CategorySettings
        return CategorySettings(self.controller, self)

    def _import_skill_settings(self):
        from app.ui.skill_settings import SkillSettings
        return SkillSettings(self.controller, self)
    
    def setup_signals(self):
        logging.debug("Setting up signals...")
        QTimer.singleShot(200, self.validate_and_connect) # 200ms後に実行
        
    def validate_and_connect(self):
        
        if not self.group_settings or not hasattr(self.group_settings, 'group_list') or not self.group_settings.group_list or not self.group_settings.group_list.count() > 0:
            logging.error("Error : No Group found")
            self.show_error("初期化に失敗しました。グループ設定が初期化されていません")
            return
        
        if not self.category_settings or not hasattr(self.category_settings, 'parent_category_list') or not self.category_settings.parent_category_list or not self.category_settings.parent_category_list.count() > 0: # ここを修正
             logging.error("Error : Parent Category not initialized")
             self.show_error("初期化に失敗しました。親カテゴリ設定が初期化されていません")
             return
        
        if not self.category_settings or not hasattr(self.category_settings, 'child_category_list') or not self.category_settings.child_category_list:
             logging.error("Error : Child Category not initialized")
             self.show_error("初期化に失敗しました。子カテゴリ設定が初期化されていません")
             return

        if not self.skill_settings or not hasattr(self.skill_settings, 'skill_group_combo') or not self.skill_settings.skill_group_combo:
              logging.error("Error : Skill Group Combo not found")
              self.show_error("初期化に失敗しました。スキルグループコンボボックスが初期化されていません")
              return

        self.group_settings.group_added.connect(self.on_group_added_handler)
        self.group_settings.group_list.currentItemChanged.connect(self.update_skill_group_combo_from_list)
        self.group_settings.group_list.currentItemChanged.connect(self.update_parent_list)
        self.category_settings.parent_category_list.currentItemChanged.connect(self.update_child_categories)
        self.category_settings.child_category_list.currentItemChanged.connect(self.update_skill_level_list)
        # SkillSettings の skill_group_combo の currentIndexChanged シグナルを update_skill_level_list スロットに接続
        self.skill_settings.skill_group_combo.currentIndexChanged.connect(self.update_skill_level_list)
        logging.debug("signals initialized.")

    def on_group_added_handler(self, group_name: str):
        self.group_added.emit(group_name)
        self.update_skill_group_combo()

    def update_skill_group_combo_from_list(self, current, previous):
        if current:
            group_name = current.text()
            self.skill_settings.skill_group_combo.setCurrentText(group_name)
            # グループ選択時に親カテゴリと子カテゴリ、スキルレベルリストを更新
            self.update_parent_list(current, previous)
            if self.category_settings.parent_category_list.count() > 0:
                self.category_settings.parent_category_list.setCurrentRow(0)
            self.update_skill_level_list()
        else:
            self.skill_settings.skill_group_combo.setCurrentIndex(-1)
            self.clear_ui_elements(self.category_settings.parent_category_list,
                self.category_settings.child_category_list,
                self.skill_settings.skill_level_list)
            if self.group_settings.group_list.count() == 0:
                self.show_error("利用可能なグループがありません。新しいグループを追加してください。")

    def update_parent_list(self, current, previous):
        self.clear_ui_elements(self.category_settings.parent_category_list,
                               self.category_settings.child_category_list,
                               self.skill_settings.skill_level_list)

        if current:
            group_name = current.text()
            skill_matrix = self.skill_matrix_model.get_skill_matrix()
            parent_categories = []
            for item in skill_matrix:
                if item.group.name == group_name and item.is_parent:
                    parent_categories.append(item.skill_name)
            if parent_categories:
                self.category_settings.parent_category_list.addItems(parent_categories)
                logging.debug(f"Updating parent list for group: {group_name}, found parents: {parent_categories}")

    def update_child_categories(self, current, previous):
        self.clear_ui_elements(self.category_settings.child_category_list,
                               self.skill_settings.skill_level_list)
        if current:
            selected_group = self.group_settings.group_list.currentItem()
            if selected_group:
                group_name = selected_group.text()
                parent_name = current.text()
                skill_matrix = self.skill_matrix_model.get_skill_matrix()

                child_categories = []
                for item in skill_matrix:
                    if item.group.name == group_name and item.parent and hasattr(item.parent, 'skill_name') and item.parent.skill_name == parent_name and not item.is_parent:
                        child_categories.append(item.skill_name)

                self.category_settings.child_category_list.addItems(child_categories)
                logging.debug(f"Updating child list for group: {group_name}, parent: {parent_name}, found children: {child_categories}")

    def update_skill_level_list(self, current=None, previous=None):
        self.skill_settings.skill_level_list.clear()
        selected_group_name, selected_parent, selected_child = self._get_selected_skill_info()

        logging.debug(
            f"Updating skill level list for group: {selected_group_name}, parent: {selected_parent}, child: {selected_child}")
        if not selected_group_name:
           logging.debug("No group selected to update skill level list.")
           return
        
        skill_levels_to_display = self.fetch_skill_levels(selected_group_name, selected_parent, selected_child)
        self._populate_skill_level_list(skill_levels_to_display)

    def _get_selected_skill_info(self) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        selected_group_name = self.skill_settings.skill_group_combo.currentText()
        selected_parent = self.category_settings.parent_category_list.currentItem()
        selected_child = self.category_settings.child_category_list.currentItem()
        return (
            selected_group_name,
            selected_parent.text() if selected_parent else None,  # 親カテゴリを文字列として返す
            selected_child.text() if selected_child else None
        )

    def fetch_skill_levels(self, group_name: str, parent_name: Optional[str], child_name: Optional[str]) -> list[str]:
        logging.debug(f"Fetching skills for group: {group_name}, parent: {parent_name}, child: {child_name}")
        skill_matrix = self.skill_matrix_model.get_skill_matrix()
        skill_levels = []

        for item in skill_matrix:
            logging.debug(f"Checking item: {item.skill_name}, group={item.group.name}, parent={item.parent.skill_name if hasattr(item,'parent') and item.parent else None}, is_parent={item.is_parent}")
            
            if item.group.name == group_name:
                if parent_name and child_name:
                    if hasattr(item, 'parent') and item.parent and hasattr(item.parent, 'skill_name') and item.parent.skill_name == parent_name and item.skill_name == child_name and not item.is_parent:
                         if item.skill_name.isdigit():
                            skill_levels.append(item.skill_name)
                elif parent_name:
                    if hasattr(item, 'parent') and item.parent and hasattr(item.parent, 'skill_name') and item.parent.skill_name == parent_name and not item.is_parent:
                         if item.skill_name.isdigit():
                             skill_levels.append(item.skill_name)
                elif not hasattr(item, 'parent') and item.skill_name.isdigit():
                    skill_levels.append(item.skill_name)

        logging.debug(f"Fetched skill levels: {skill_levels}")
        return skill_levels


    def _populate_skill_level_list(self, skill_levels: list[str]):
        max_skill_level = 0
        for level in skill_levels:
          # 数値のスキルレベルのみ追加
          if level.isdigit():
              self.skill_settings.skill_level_list.addItem(level)
              max_skill_level = max(max_skill_level, int(level))
        
        # 最大のスキルレベルを選択
        if max_skill_level > 0:
            self.skill_settings.skill_level_combo.setCurrentText(str(max_skill_level))
        else:
            self.skill_settings.skill_level_combo.setCurrentText("1")

    def clear_ui_elements(self, *widgets):
        for widget in widgets:
            widget.clear()

    def show_error(self, message: str):
        full_message = f"エラー: {message}"
        QMessageBox.critical(self, "エラー", full_message)
        logging.error(full_message)