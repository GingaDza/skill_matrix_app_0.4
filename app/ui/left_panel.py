# app/ui/left_panel.py
import logging
# PyQt5に変更
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QComboBox, QMessageBox, QDialog
from PyQt5.QtCore import Qt # Qt をインポート

from app.ui.dialogs import AddParticipantDialog
from app.models.skill_matrix_model import SkillMatrix


# ログの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LeftPanel(QWidget):
    def __init__(self, controller, initial_settings_tab):
        super().__init__()
        logger.debug("Initializing LeftPanel...")
        self.controller = controller
        self.initial_settings_tab = initial_settings_tab

        # メインレイアウト
        main_layout = QVBoxLayout(self)

        # グループ選択コンボボックス
        group_label = QLabel("グループ選択:")
        self.group_combo = QComboBox()
        group_layout = QHBoxLayout()
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_combo)
        main_layout.addLayout(group_layout)

        # 参加者リスト
        self.participants_list = QListWidget()
        self.participant_add_button = QPushButton("新規")
        self.participant_save_button = QPushButton("編集")
        self.participant_delete_button = QPushButton("削除")
        self.participant_screen_button = QPushButton("スクリーンショット")

        # ボタンレイアウト（参加者操作ボタンを縦に並べる）
        participant_button_layout = QVBoxLayout()
        participant_button_layout.addWidget(self.participant_add_button)
        participant_button_layout.addWidget(self.participant_save_button)
        participant_button_layout.addWidget(self.participant_delete_button)
        participant_button_layout.addWidget(self.participant_screen_button)

        # 参加者リストと操作ボタンを縦に並べる
        participant_layout = QVBoxLayout()
        participant_layout.addWidget(QLabel("参加者"))
        participant_layout.addWidget(self.participants_list)
        participant_layout.addLayout(participant_button_layout)
        main_layout.addLayout(participant_layout)

        # イベント接続
        self.participant_add_button.clicked.connect(self.on_add_participant)
        self.participant_save_button.clicked.connect(self.on_save_participant)
        self.participant_delete_button.clicked.connect(self.on_delete_participant)
        self.participant_screen_button.clicked.connect(self.on_participant_screen_shot)
        self.group_combo.currentIndexChanged.connect(self.update_participants_list)
        self.group_combo.currentIndexChanged.connect(self.update_initial_settings_tab_group)

        self.setLayout(main_layout)

        # データベース接続とビュー更新
        self.setup_group_combo()
        logger.debug("LeftPanel initialized.")

    def setup_group_combo(self):
        try:
            skill_matrix = self.initial_settings_tab.skill_matrix_model.get_skill_matrix()
            logger.debug(f"Retrieved skill matrix: {skill_matrix}")

            groups = []
            for item in skill_matrix:
                if item.group and item.group.name not in groups:
                    groups.append(item.group.name)

            selected_group = self.group_combo.currentText()
            self.group_combo.clear()
            self.group_combo.addItems(groups)

            if selected_group and selected_group in groups:
                index = self.group_combo.findText(selected_group)
                if index != -1:
                   self.group_combo.setCurrentIndex(index)

            logger.debug(f"Groups found: {groups}")

        except Exception as e:
            logger.error(f"Error updating group combo box: {e}")
            self.group_combo.clear()

# app/ui/left_panel.py
# app/ui/left_panel.py
# app/ui/left_panel.py
    def update_participants_list(self, index):
        self.participants_list.clear()
        selected_group_name = self.group_combo.itemText(index) if index >= 0 else None
        if selected_group_name:
            skill_matrix = self.initial_settings_tab.skill_matrix_model.get_skill_matrix()
            participants = [
                item.skill_name
                for item in skill_matrix
                if item.group
                and item.group.name == selected_group_name
                and not item.is_parent
                and (not hasattr(item, 'parent') or item.parent is None ) # ここを修正
            ]

            if participants:
                self.participants_list.addItems(participants)
                logger.debug(f"Updating participants list for group: {selected_group_name}, found participants: {participants}")

    def update_initial_settings_tab_group(self, index):
        selected_group_name = self.group_combo.itemText(index) if index >= 0 else None
        if selected_group_name:
            items = self.initial_settings_tab.group_settings.group_list.findItems(selected_group_name, Qt.MatchFlag.MatchExactly)
            if items:
                self.initial_settings_tab.group_settings.group_list.setCurrentItem(items[0])

    def on_add_participant(self):
        logger.debug("Add participant clicked")
        selected_group_name = self.group_combo.currentText()
        if not selected_group_name:
            self.show_error("グループを選択してください。")
            return

        dialog = AddParticipantDialog(self, "新しい参加者を追加", selected_group_name)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_participant_name = dialog.get_input_text()
            if new_participant_name:
                if self.initial_settings_tab.skill_matrix_model.add_participant(selected_group_name, new_participant_name):
                    self.update_participants_list(self.group_combo.currentIndex())
                else:
                    self.show_error("参加者の追加に失敗しました")

            else:
                self.show_error("参加者名を入力してください")

    def on_save_participant(self):
        logger.debug("Save participant clicked")
        selected_item = self.participants_list.currentItem()
        selected_group_name = self.group_combo.currentText()
        if not selected_item:
            self.show_error("編集する参加者を選択してください。")
            return
        if not selected_group_name:
            self.show_error("グループを選択してください")
            return
        participant_name = selected_item.text()
        dialog = AddParticipantDialog(self, "参加者名を編集", selected_group_name, initial_text=participant_name)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_participant_name = dialog.get_input_text()
            if new_participant_name:
                if self.initial_settings_tab.skill_matrix_model.rename_participant(selected_group_name, participant_name, new_participant_name):
                    selected_item.setText(new_participant_name)
                    self.update_participants_list(self.group_combo.currentIndex())
                else:
                    self.show_error("参加者名の編集に失敗しました")
            else:
                self.show_error("参加者名を入力してください。")

    def on_delete_participant(self):
        logger.debug("Delete participant clicked")
        selected_item = self.participants_list.currentItem()
        selected_group_name = self.group_combo.currentText()
        if not selected_item:
            self.show_error("削除する参加者を選択してください。")
            return
        if not selected_group_name:
            self.show_error("グループを選択してください。")
            return
        participant_name = selected_item.text()
        if QMessageBox.question(self, "削除確認", f"参加者 '{participant_name}' を削除しますか？") == QMessageBox.StandardButton.Yes:
            if self.initial_settings_tab.skill_matrix_model.delete_participant(selected_group_name, participant_name):
                self.participants_list.takeItem(self.participants_list.row(selected_item))
            else:
                self.show_error("参加者の削除に失敗しました")

    def on_participant_screen_shot(self):
        logger.debug("Screen shot clicked")
        selected_item = self.participants_list.currentItem()
        if not selected_item:
            self.show_error("スクリーンショットする参加者を選択してください。")
            return
        print(f"Screen shot for {selected_item.text()}")

    def show_error(self, message):
        logger.error(f"Error: {message}")
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("エラー")
        error_dialog.exec()