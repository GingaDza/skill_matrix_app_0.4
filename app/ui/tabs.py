# app/ui/tabs.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QHBoxLayout, QScrollArea # noqa: E402
from app.models.skill_matrix_model import SkillMatrix  # 修正したインポート

class CustomTab(QWidget):
    def __init__(self, parent, group_name):
        super().__init__(parent)
        self.group_name = group_name  # グループ名の保存

        # メインレイアウト
        layout = QVBoxLayout(self)

        # グループ名ラベル
        group_label = QLabel(f"Group: {group_name}")
        layout.addWidget(group_label)

        # スキル選択コンボボックス
        self.skill_combo = QComboBox()
        layout.addWidget(self.skill_combo)

        # スキルを表示するスクロールエリア
        scroll_area = QScrollArea()
        layout.addWidget(scroll_area)

        # スキル追加ボタン
        self.add_skill_button = QPushButton("Add Skill")
        layout.addWidget(self.add_skill_button)

        # スキルボタンイベント
        self.add_skill_button.clicked.connect(self.on_add_skill)

        self.setLayout(layout)

    def on_add_skill(self):
        print(f"Adding skill for group: {self.group_name}")
        # スキル追加処理を書く場合はここに実装
